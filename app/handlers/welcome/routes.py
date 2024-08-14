from aiogram import types, Router, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.config import settings
from app.database import storage
from app.handlers import welcome, travel, personal, admin
from app.models import RoleEnum

router = Router()


def get_help_message() -> str:
    help_message = "Доступные команды:\n"
    for command, description in welcome.AllCommandSchema().model_dump().items():
        help_message += f"/{command} - {description}\n"

    return help_message


@router.message(Command("start"))
async def get_start(message: types.Message, bot: Bot, nickname: str) -> None:
    photo = types.FSInputFile(settings.STATIC_STORAGE / "hello.webp")
    await bot.send_photo(chat_id=message.chat.id,
                         photo=photo,
                         caption=f"*Привет, {nickname}! Чем сегодня займёмся?*☺️",
                         reply_markup=welcome.welcome_keyboard(),
                         parse_mode="Markdown")
    await message.delete()


@router.callback_query(F.data == "welcome:help::::")
async def help_callback(callback: types.CallbackQuery, bot: Bot) -> None:
    media = types.FSInputFile(settings.STATIC_STORAGE / "help.webp")
    help_message = get_help_message()
    await callback.answer("Отправляю список доступные команд")
    await bot.send_photo(chat_id=callback.from_user.id,
                         photo=media,
                         caption=help_message)


@router.message(Command("help"))
async def get_help(message: types.Message) -> None:
    media = types.FSInputFile(settings.STATIC_STORAGE / "help.webp")
    help_message = get_help_message()
    await message.answer_photo(photo=media,
                               caption=help_message)


@router.callback_query(F.data == "welcome::registration:::")
async def register_callback(callback: types.CallbackQuery) -> None:
    if await storage.get_user(user_id=callback.from_user.id):
        await callback.answer(text="Пользователь с таким telegramID уже существует",
                              show_alert=True)
        return None

    user = welcome.AddUserSchema(
        telegram_id=callback.from_user.id,
        full_name=callback.from_user.full_name,
        username=callback.from_user.username,
        nickname=callback.from_user.full_name
    )
    await storage.add_user(user=user)
    await callback.answer(text=f"Успешно создали нового пользователя {user.full_name} c telegramID: {user.telegram_id}",
                          show_alert=True)


@router.callback_query(F.data == "welcome:::personal::")
async def personal_callback(callback: types.CallbackQuery, bot: Bot) -> None:
    user = await storage.get_user(user_id=callback.from_user.id)
    if not user or user.is_active is False:
        await callback.answer(text="Раздел 'личный кабинет' только для зарегистрированных пользователей!",
                              show_alert=True)
        return None

    await callback.answer(text="Переходим в личный кабинет")
    photo = types.FSInputFile(settings.STATIC_STORAGE / "personal.webp")
    if callback.message:
        await bot.send_photo(chat_id=callback.message.chat.id,
                             photo=photo,
                             caption="*Что хотите сделать в личном кабинете?*☺️",
                             reply_markup=personal.personal_keyboard(),
                             parse_mode="Markdown")


@router.callback_query(F.data == "welcome::::travel:")
async def travel_callback(callback: types.CallbackQuery, bot: Bot, nickname: str) -> None:
    await callback.answer("Переходим в блок о путешествиях")
    photo = types.FSInputFile(settings.STATIC_STORAGE / "travel.webp")
    if callback.message:
        await bot.send_photo(chat_id=callback.message.chat.id,
                             photo=photo,
                             caption=f"*Что хотите сделать в разделе путешествий, {nickname}?*☺️",
                             reply_markup=travel.travel_keyboard(),
                             parse_mode="Markdown")


@router.callback_query(F.data == "welcome:::::admin")
async def admin_callback(callback: types.CallbackQuery, bot: Bot, nickname: str) -> None:
    user = await storage.get_user(user_id=callback.from_user.id)
    if not user or user.role != RoleEnum.admin or user.is_active is False:
        await callback.answer(text="Недостаточно прав!",
                              show_alert=True)
        return None

    await callback.answer("Переходим в раздел для администрации")
    photo = types.FSInputFile(settings.STATIC_STORAGE / "admin.webp")
    if callback.message:
        await bot.send_photo(chat_id=callback.message.chat.id,
                             photo=photo,
                             caption="*Кого нужно отадминистрировать?*👀",
                             reply_markup=admin.admin_keyboard(),
                             parse_mode="Markdown")


@router.message(Command("cancel"))
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state:
        await state.clear()

    await message.answer(
        text="Отменено",
        reply_markup=types.ReplyKeyboardRemove(),
    )

# @router.callback_query()
# async def all_callback(callback: types.CallbackQuery):
#     print(callback.data)
#     print("фигня")
#     await callback.answer(text="фигня")
