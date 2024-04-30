from datetime import datetime

from aiogram import types, Router, Bot, F
from aiogram.fsm.context import FSMContext

from app import keyboards, schemas, exceptions
from app.config import settings
from app.database import storage
from app.external.geodata import geocoding, distance

router = Router()


@router.callback_query(F.data == "welcome:::add_travel:")
async def travel_callback(callback: types.CallbackQuery, bot: Bot) -> None:
    await callback.answer("Переходим в блок о путешествиях")
    photo = types.FSInputFile(settings.STATIC_STORAGE / "travel.webp")
    if callback.message:
        await bot.send_photo(chat_id=callback.message.chat.id,
                             photo=photo,
                             caption="*Что хотите сделать в разделе путешествий?*☺️",
                             reply_markup=keyboards.make_travel(),
                             parse_mode="Markdown")


@router.callback_query(F.data == "travel:add_travel:")
async def add_travel_callback(callback: types.CallbackQuery, bot: Bot, state: FSMContext) -> None:
    if not await storage.get_user(user_id=callback.from_user.id):
        await callback.answer(text="Создать путешествие могут только зарегистрированные пользователи!",
                              show_alert=True)
        await state.clear()
        if callback.message:
            await bot.delete_message(chat_id=callback.from_user.id,
                                     message_id=callback.message.message_id)
        return None

    await callback.answer("Приступим!")
    await bot.send_message(chat_id=callback.from_user.id,
                           text="Выберите язык для идентификации городов",
                           reply_markup=keyboards.make_language())
    await state.set_state(schemas.LoadTrip.LANGUAGE)


@router.message(schemas.LoadTrip.LANGUAGE)
async def get_language(message: types.Message, state: FSMContext) -> None:
    language = message.text
    await message.answer(f"Вы выбрали {language} язык. Какой первый город?")
    await state.update_data(language=language)
    await state.set_state(schemas.LoadTrip.FIRST_PLACE)


@router.message(schemas.LoadTrip.FIRST_PLACE)
async def get_first_place(message: types.Message, state: FSMContext) -> None:
    first_place = message.text
    await message.answer(f"Первый город - {first_place}. Какой второй город?")
    await state.update_data(first_place=first_place)
    await state.set_state(schemas.LoadTrip.LAST_PLACE)


@router.message(schemas.LoadTrip.LAST_PLACE)
async def get_second_place(message: types.Message, state: FSMContext) -> None:
    last_place = message.text
    current_state: dict = await state.get_data()
    if last_place == current_state["first_place"]:
        await message.answer(text="Нельзя создать путешествие между двумя одинаковыми местами")
        return None

    await message.answer(f"Второй город - {last_place}. Какой вид транспорта?",
                         reply_markup=keyboards.make_transport_type())
    await state.update_data(last_place=last_place)
    await state.set_state(schemas.LoadTrip.TRANSPORT_TYPE)


@router.message(schemas.LoadTrip.TRANSPORT_TYPE)
async def get_transport_type(message: types.Message, state: FSMContext) -> None:
    transport = message.text
    await message.answer(f"Вид транспорта - {transport}. В каком году было путешествие?")
    await state.update_data(transport=transport)
    await state.set_state(schemas.LoadTrip.TRAVEL_YEAR)


@router.message(schemas.LoadTrip.TRAVEL_YEAR)
async def get_travel_year(message: types.Message, state: FSMContext) -> None:
    year = message.text
    if year and int(year) > datetime.now().year:
        await message.answer("Вы пытаетесь создать путешествие в будущем. Похвально, но невозможно.")
        await state.clear()

    await message.answer(f"Год путешествия - {year}.")
    await state.update_data(year=year)
    travel_schema = schemas.NewTravelContext(**await state.get_data())

    try:
        first_place_data = await geocoding.get_geographic_data(
            address=travel_schema.first_place,
            language=travel_schema.language)
        second_place_data = await geocoding.get_geographic_data(
            address=travel_schema.last_place,
            language=travel_schema.language)
    except exceptions.NoGeographicDataException as err:
        await message.answer(text=f"{err.message}. Попробуйте поменять язык, или изменить название.")
        return None

    trip_distance = await distance.get_distance(lat_1=first_place_data.latitude,
                                                long_1=first_place_data.longitude,
                                                lat_2=second_place_data.latitude,
                                                long_2=second_place_data.longitude)
    travel = schemas.AddTravelSchema(
        distance=trip_distance["distance"],
        transport_type=travel_schema.transport,
        travel_year=travel_schema.year,
        user_id=message.from_user.id,  # type: ignore
        location={
            travel_schema.first_place: first_place_data.country,
            travel_schema.last_place: second_place_data.country,
        }
    )

    await storage.add_new_travel(new_travel_schema=travel)
    await state.clear()
    await message.answer(text="Путешествие успешно добавлено👍")


@router.callback_query(F.data == "travel::get_travel")
async def get_travel_callback(callback: types.CallbackQuery, bot: Bot) -> None:
    if not await storage.get_user(user_id=callback.from_user.id):
        await callback.answer(
            text="Получить информацию о своих путешествиях могут только зарегистрированные пользователи!",
            show_alert=True
        )
        if callback.message:
            await bot.delete_message(chat_id=callback.from_user.id,
                                     message_id=callback.message.message_id)
        return None

    if isinstance(callback.message, types.Message):
        await callback.message.edit_caption(caption="Чуть-чуть конкретней😌",
                                            reply_markup=keyboards.make_get_travel())


@router.callback_query(F.data == "my_travel:get_travel::")
async def get_all_travels_callback(callback: types.CallbackQuery, bot: Bot) -> None:
    all_travels = [
        schemas.GetTravelSchema(
            travel_id=travel.travel_id,
            distance=travel.distance,
            transport_type=travel.transport_type,
            travel_year=travel.travel_year,
            location=travel.location,
        ) for travel in await storage.get_all_travels(user_id=callback.from_user.id)
    ]
    response = "*Предоставляю информацию по путешествиям*"
    for travel in all_travels:
        response += f"""
        *TravelID:* {travel.travel_id}
        *Distance:* {travel.distance}
        *Transport Type:* {travel.transport_type}
        *Travel Year:* {travel.travel_year}
        *Location:* {travel.location}
        """

    await callback.answer(text="Информация получена")
    await bot.send_message(chat_id=callback.from_user.id,
                           text=response,
                           parse_mode="Markdown")


@router.callback_query(F.data == "my_travel::get_distance:")
async def get_distance_callback(callback: types.CallbackQuery, bot: Bot) -> None:
    air_distance = await storage.get_distance(user_id=callback.from_user.id,
                                              transport_type="Воздушный")
    ground_distance = await storage.get_distance(user_id=callback.from_user.id,
                                                 transport_type="Наземный")
    response = f"""
    *Предоставляю информацию по дистанции:*
    *Дистанция по воздуху:* {air_distance} километров
    *Дистанция по земле:* {ground_distance} километров
    *Всего проехал:* {air_distance + ground_distance} километров
    """
    await callback.answer(text="Информация получена")
    await bot.send_message(chat_id=callback.from_user.id,
                           text=response,
                           parse_mode="Markdown")


@router.callback_query(F.data == "my_travel:::get_country")
async def get_country_callback(callback: types.CallbackQuery, bot: Bot) -> None:
    countries = await storage.get_all_countries(user_id=callback.from_user.id)
    for i in countries:
        print(i)
