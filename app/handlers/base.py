from aiogram import types, Router, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app import keyboards
from app.config import settings
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
    photo = types.FSInputFile(settings.STATIC_STORAGE / "hello.jpg")
    await bot.send_photo(chat_id=message.chat.id,
                         photo=photo,
                         caption="*Привет! Чем сегодня займёмся?*☺️",
                         reply_markup=keyboards.make_start())
    await message.delete()


@router.message(Command("help"))
async def get_help(message: types.Message) -> None:
    media = types.FSInputFile(settings.STATIC_STORAGE / "help.png")
    help_message = get_help_message()
    await message.answer_photo(photo=media,
                               caption=help_message)


@router.callback_query(F.data == "welcome:help::")
async def help_callback(callback: types.CallbackQuery, bot: Bot) -> None:
    media = types.FSInputFile(settings.STATIC_STORAGE / "help.png")
    help_message = get_help_message()
    await callback.answer("Отправляю список доступные команд")
    await bot.send_photo(chat_id=callback.from_user.id,
                         photo=media,
                         caption=help_message)

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
