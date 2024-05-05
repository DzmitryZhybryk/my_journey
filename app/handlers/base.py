from aiogram import types, Router, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app import keyboards
from app import schemas
from app.config import settings
from app.database import storage
from app.schemas.keyboard import AllCommandSchema

router = Router()


@router.message(Command("cancel"))
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state:
        await state.clear()

    await message.answer(
        text="Отменено",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@router.message(Command("start"))
async def get_start(message: types.Message, bot: Bot) -> None:
    photo = types.FSInputFile(settings.STATIC_STORAGE / "hello.webp")
    if message.from_user:  # TODO сделать через middleware
        current_user = await storage.get_user(user_id=message.from_user.id)
        user = current_user.full_name if current_user else "Семпай"
        await bot.send_photo(chat_id=message.chat.id,
                             photo=photo,
                             caption=f"*Привет, {user}! Чем сегодня займёмся?*☺️",
                             reply_markup=keyboards.make_start(),
                             parse_mode="Markdown")
        await message.delete()


@router.message(Command("help"))
async def get_help(message: types.Message) -> None:
    media = types.FSInputFile(settings.STATIC_STORAGE / "help.webp")
    help_message = get_help_message()
    await message.answer_photo(photo=media,
                               caption=help_message)


@router.callback_query(F.data == "welcome:help:::")
async def help_callback(callback: types.CallbackQuery, bot: Bot) -> None:
    media = types.FSInputFile(settings.STATIC_STORAGE / "help.webp")
    help_message = get_help_message()
    await callback.answer("Отправляю список доступные команд")
    await bot.send_photo(chat_id=callback.from_user.id,
                         photo=media,
                         caption=help_message)


@router.callback_query(F.data == "welcome::::registration")
async def register_callback(callback: types.CallbackQuery) -> None:
    if await storage.get_user(user_id=callback.from_user.id):
        await callback.answer(text="Пользователь с таким telegramID уже существует",
                              show_alert=True)
        return None

    user = schemas.AddUserSchema(
        telegram_id=callback.from_user.id,
        full_name=callback.from_user.full_name,
        username=callback.from_user.username,
        nickname=callback.from_user.full_name
    )
    await storage.add_user(user=user)
    await callback.answer(text=f"Успешно создали нового пользователя {user.full_name} c telegramID: {user.telegram_id}",
                          show_alert=True)


# @router.callback_query()
# async def all_callback(callback: types.CallbackQuery):
#     print(callback.data)
#     print("фигня")
#     await callback.answer(text="фигня")


def get_help_message() -> str:
    help_message = "Доступные команды:\n"
    for command, description in AllCommandSchema().model_dump().items():
        help_message += f"/{command} - {description}\n"

    return help_message
