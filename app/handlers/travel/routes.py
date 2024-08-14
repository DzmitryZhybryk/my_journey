from datetime import datetime

from aiogram import types, Router, Bot, F
from aiogram.fsm.context import FSMContext
from jinja2 import Template

from app import exceptions
from app.database import storage
from app.external.geodata import geocoding, distance
from app.handlers import travel
from app.utils import funcs

router = Router()


@router.callback_query(F.data == "travel:add_travel::")
async def add_travel_callback(callback: types.CallbackQuery, bot: Bot, state: FSMContext) -> None:
    await callback.answer("Приступим!")
    await bot.send_message(chat_id=callback.from_user.id,
                           text="Какой первый город?")
    await state.set_state(travel.LoadTrip.FIRST_PLACE)


@router.message(travel.LoadTrip.FIRST_PLACE)
async def get_first_place(message: types.Message, state: FSMContext) -> None:
    first_place = message.text
    await message.answer(f"Первый город - {first_place}. Какой второй город?")
    await state.update_data(first_place=first_place)
    await state.set_state(travel.LoadTrip.LAST_PLACE)


@router.message(travel.LoadTrip.LAST_PLACE)
async def get_second_place(message: types.Message, state: FSMContext) -> None:
    second_place = message.text
    current_state: dict = await state.get_data()
    if second_place == current_state["first_place"]:
        await message.answer(text="Нельзя создать путешествие между двумя одинаковыми местами")
        return None

    await message.answer(f"Второй город - {second_place}. Какой вид транспорта?",
                         reply_markup=travel.transport_type_keyboard())
    await state.update_data(second_place=second_place)
    await state.set_state(travel.LoadTrip.TRANSPORT_TYPE)


@router.message(travel.LoadTrip.TRANSPORT_TYPE)
async def get_transport_type(message: types.Message, state: FSMContext) -> None:
    transport = message.text
    await message.answer(f"Вид транспорта - {transport}. В каком году было путешествие?")
    await state.update_data(transport=transport)
    await state.set_state(travel.LoadTrip.TRAVEL_YEAR)


@router.message(travel.LoadTrip.TRAVEL_YEAR)
async def get_travel_year(message: types.Message, state: FSMContext) -> None:
    year = message.text
    if year and int(year) > datetime.now().year:
        await message.answer("Вы пытаетесь создать путешествие в будущем. Похвально, но невозможно.")
        await state.clear()

    await message.answer(f"Год путешествия - {year}.")
    await state.update_data(year=year)

    travel_schema = travel.NewTravelContext(**await state.get_data())

    try:
        first_place_data = await geocoding.get_geographic_data(city=travel_schema.first_place)
        second_place_data = await geocoding.get_geographic_data(city=travel_schema.second_place)
    except exceptions.NoGeographicDataException as err:
        await message.answer(text=f"{err.message}. Попробуйте поменять язык, или изменить название.")
        return None
    except exceptions.ExternalServiceError:
        await message.answer(text="Ошибка сервиса при получении геоданных. Попробуйте позже")
        return None

    trip_distance = await distance.get_distance(lat_1=first_place_data.latitude,
                                                long_1=first_place_data.longitude,
                                                lat_2=second_place_data.latitude,
                                                long_2=second_place_data.longitude)
    my_travel = travel.AddTravelSchema(
        distance=trip_distance["distance"],
        transport_type=travel_schema.transport,
        travel_year=travel_schema.year,
        user_id=message.from_user.id,  # type: ignore
        location=travel.LocationSchema(
            from_=travel.PointSchema(
                town=travel_schema.first_place,
                country=first_place_data.country,
            ),
            to=travel.PointSchema(
                town=travel_schema.second_place,
                country=second_place_data.country,
            )
        )
    )

    await storage.add_new_travel(new_travel_schema=my_travel)
    response = f"""
    *Новое путешествие:*
    Из {my_travel.location.from_.town}, {my_travel.location.from_.country}
    В {my_travel.location.to.town}, {my_travel.location.to.country} 
    успешно добавлено👍
    """
    await message.answer(text=response,
                         parse_mode="Markdown")
    await state.clear()
    await message.answer(text="Хотите добавить еще путешествие?",
                         reply_markup=travel.one_more_travel_keyboard())


@router.callback_query(F.data == "travel::get_travel:")
async def get_travel_callback(callback: types.CallbackQuery) -> None:
    if isinstance(callback.message, types.Message):
        await callback.message.edit_caption(caption="Чуть-чуть конкретней😌",
                                            reply_markup=travel.get_travel_keyboard())


@router.callback_query(F.data == "my_travel:get_travel:::")
async def get_all_travels_callback(callback: types.CallbackQuery, bot: Bot) -> None:
    all_travels = [
        travel.GetTravelSchema(
            travel_id=travels.travel_id,
            distance=travels.distance,
            transport_type=travels.transport_type,
            travel_year=travels.travel_year,
            location=travels.location,  # type: ignore
        ) for travels in await storage.get_all_travels(user_id=callback.from_user.id)
    ]

    response = "\n\n".join(
        f"*TravelID:* {item.travel_id}\n"
        f"*From:* {item.location.from_.town}, {item.location.from_.country}\n"
        f"*To:* {item.location.to.town}, {item.location.to.country}\n"
        f"*Distance:* {item.distance}\n"
        f"*Transport type:* {item.transport_type}\n"
        f"*Year:* {item.travel_year}"
        for item in all_travels
    )

    await funcs.send_long_message(chat_id=callback.from_user.id,
                                  text=response,
                                  bot=bot,
                                  parse_mode="Markdown")


@router.callback_query(F.data == "my_travel::get_distance::")
async def get_distance_callback(callback: types.CallbackQuery, bot: Bot) -> None:
    air_distance = await storage.get_distance(user_id=callback.from_user.id,
                                              transport_type="Воздушный")
    ground_distance = await storage.get_distance(user_id=callback.from_user.id,
                                                 transport_type="Наземный")
    template = Template("""
    <b>Предоставляю информацию по дистанции</b>:
    <b>Дистанция по воздуху:</b> {{ air_distance }} километров
    <b>Дистанция по земле:</b> {{ ground_distance }} километров
    <b>Общая дистанция:</b> {{ result }} километров
    """) if air_distance or ground_distance else Template("К сожалению, вы пока не добавили никаких путешествий😢")
    response = template.render(air_distance=air_distance,
                               ground_distance=ground_distance,
                               result=air_distance + ground_distance)
    await callback.answer(text="Информация получена")
    await bot.send_message(chat_id=callback.from_user.id,
                           text=response,
                           parse_mode="HTML")


@router.callback_query(F.data == "my_travel:::get_country:")
async def get_country_callback(callback: types.CallbackQuery, bot: Bot) -> None:
    countries = await storage.get_all_countries(user_id=callback.from_user.id)
    template = Template("""
    <b>Предоставляю информацию по странам</b>:{% for country in countries %}
    {{ loop.index }}.{{ country[0] }}{% endfor %}
    """) if countries else Template("К сожалению, вы пока не добавили никаких путешествий😢")
    response = template.render(countries=countries)
    await callback.answer(text="Информация получена")
    await bot.send_message(chat_id=callback.from_user.id,
                           text=response,
                           parse_mode="HTML")


@router.callback_query(F.data == "my_travel::::get_detail")
async def get_detail_callback(callback: types.CallbackQuery, bot: Bot) -> None:
    air_distance = await storage.get_distance(user_id=callback.from_user.id,
                                              transport_type="Воздушный")
    ground_distance = await storage.get_distance(user_id=callback.from_user.id,
                                                 transport_type="Наземный")
    air_travel_count = await storage.get_travel_count(user_id=callback.from_user.id,
                                                      transport_type="Воздушный")
    ground_travel_count = await storage.get_travel_count(user_id=callback.from_user.id,
                                                         transport_type="Наземный")
    all_countries = await storage.get_all_countries(user_id=callback.from_user.id)
    template = Template("""
        <b>Предоставляю подробную информация о ваших путешествиях</b>:
        <b>Всего совершено:</b> {{ total_travel }} поездок, общей дистанцией {{ total_distance }} километров
        <b>Из них по земле:</b> {{ ground_travel_count }} поездок, дистанция {{ ground_distance }} километров
        <b>По воздуху:</b> {{ air_travel_count }} поездок, дистанция {{ air_distance }} километров
        <b>Всего стран посетил:</b> {{ total_country_count }} стран
        """) if air_distance or ground_distance else Template("К сожалению, вы пока не добавили никаких путешествий😢")
    response = template.render(total_travel=air_travel_count + ground_travel_count,
                               total_distance=air_distance + ground_distance,
                               ground_travel_count=ground_travel_count,
                               ground_distance=ground_distance,
                               air_travel_count=air_travel_count,
                               air_distance=air_distance,
                               total_country_count=len(all_countries))
    await callback.answer(text="Информация получена")
    await bot.send_message(chat_id=callback.from_user.id,
                           text=response,
                           parse_mode="HTML")


@router.callback_query(F.data == "travel:::delete_travel")
async def delete_travel_callback(callback: types.CallbackQuery, bot: Bot, state: FSMContext) -> None:
    await callback.answer("Удаляем путешествие. Будьте внимательны!")
    await bot.send_message(chat_id=callback.from_user.id,
                           text="Введите TravelID путешествия, которое хотите удалить")
    await state.set_state(travel.DeleteTrip.TRAVEL_ID)


@router.message(travel.DeleteTrip.TRAVEL_ID)
async def delete_travel(message: types.Message) -> None:
    if message.from_user and message.text:
        travel_id = int(message.text)
        travel = await storage.get_travel_by_id(travel_id=travel_id)
        if not travel:
            await message.answer(text=f"Путешествие с TravelID {travel_id} не найдено")
            return None

        if travel.deleted_date:
            await message.answer(text=f"Путешествие с TravelID {travel_id} уже удалено")
            return None

        await storage.delete_travel(travel_id=travel_id, user_id=message.from_user.id)
        await message.answer(text=f"Путешествие с TravelID {travel_id} успешно удалено")
