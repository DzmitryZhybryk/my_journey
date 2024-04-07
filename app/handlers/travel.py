from datetime import datetime

from aiogram import types, Router, Bot, F
from aiogram.fsm.context import FSMContext

from app import keyboards
from app import schemas
from app.config import settings

router = Router()


@router.callback_query(F.data == "welcome:travel::")
async def travel_callback(callback: types.CallbackQuery, bot: Bot) -> None:
    await callback.answer("Переходим в блок о путешествиях")
    photo = types.FSInputFile(settings.STATIC_STORAGE / "travel.jpg")
    if callback.message:
        await bot.send_photo(chat_id=callback.message.chat.id,
                             photo=photo,
                             caption="*Что хотите сделать в разделе путешествий?*☺️",
                             reply_markup=keyboards.make_travel())


@router.callback_query(F.data == "travel:add_travel:")
async def add_travel_callback(callback: types.CallbackQuery, bot: Bot, state: FSMContext) -> None:
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
    context_data = await state.get_data()
    print(context_data)
    await state.clear()
