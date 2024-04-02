from aiogram import types, Router, Bot, F
from aiogram.filters import Command

from app.keyboards.welcome import get_welcome_keyboard, get_about_me_keyboard
from app.keyboards.schemas import AllCommandSchema
from app.config import settings

router = Router()


@router.message(Command('start'))
async def get_start(message: types.Message, bot: Bot):
    photo = types.FSInputFile(settings.STATIC_STORAGE / "hello.jpg")
    await bot.send_photo(chat_id=message.chat.id,
                         photo=photo,
                         caption="*Привет! Чем сегодня займёмся?*☺️",
                         parse_mode="Markdown",
                         reply_markup=get_welcome_keyboard())
    await message.delete()


@router.message(Command('help'))
async def get_help(message: types.Message) -> None:
    media = types.FSInputFile(settings.STATIC_STORAGE / "help.png")
    help_message = get_help_message()
    await message.answer_photo(photo=media,
                               caption=help_message)


@router.message(Command('about_me'))
async def about_me(message: types.Message):
    await message.answer(text="Какие данные тебе нужны?", reply_markup=get_about_me_keyboard())


@router.callback_query(F.data == "welcome:help::")
async def help_callback(callback: types.CallbackQuery, bot: Bot):
    media = types.FSInputFile(settings.STATIC_STORAGE / "help.png")
    help_message = get_help_message()
    await callback.answer("Отправляю список доступные команд")
    await bot.send_photo(chat_id=callback.from_user.id,
                         photo=media,
                         caption=help_message)


@router.callback_query(F.data == "welcome::about_me:")
async def about_me_callback(callback: types.CallbackQuery, bot: Bot):
    await callback.answer("Что именно вас интересует?")
    await bot.send_message(chat_id=callback.from_user.id,
                           text="Что именно вас интересует?",
                           reply_markup=get_about_me_keyboard())

@router.callback_query()
async def all_callback(callback: types.CallbackQuery):
    print(callback.data)
    print("фигня")
    await callback.answer(text="фигня")


def get_help_message() -> str:
    help_message = "Доступные команды:\n"
    for command, description in AllCommandSchema().model_dump().items():
        help_message += f"/{command} - {description}\n"

    return help_message

# @router.callback_query()
# async def get_start_callback(call: types.CallbackQuery, bot: Bot):
#     await call.answer(answer)
#     await bot.edit_message_text(text=all_answers.main_menu_message,
#                                 chat_id=call.from_user.id,
#                                 message_id=call.message.message_id,
#                                 reply_markup=get_main_keyboard())
