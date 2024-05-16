from aiogram import types, Bot
from aiogram.filters.callback_data import CallbackData

from app.config import settings
from app.handlers import welcome


class ReturnKeyboardSchema(CallbackData, prefix="return"):
    to_welcome: str | None = None


async def return_to_base(callback: types.CallbackQuery, bot: Bot, nickname: str) -> None:
    await callback.answer("Возвращаемся на главную")
    photo = types.FSInputFile(settings.STATIC_STORAGE / "hello.webp")
    await bot.send_photo(chat_id=callback.from_user.id,
                         photo=photo,
                         caption=f"*Привет, {nickname}! Чем сегодня займёмся?*☺️",
                         reply_markup=welcome.welcome_keyboard(),
                         parse_mode="Markdown")
