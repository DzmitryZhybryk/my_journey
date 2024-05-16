from aiogram import types, Router, Bot, F

from app.config import settings
from app.handlers import welcome

router = Router()


@router.callback_query(F.data == "return:to_welcome")
async def return_to_base_callback(callback: types.CallbackQuery, bot: Bot, nickname: str) -> None:
    await callback.answer("Возвращаемся на главную")
    photo = types.FSInputFile(settings.STATIC_STORAGE / "hello.webp")
    await bot.send_photo(chat_id=callback.from_user.id,
                         photo=photo,
                         caption=f"*Привет, {nickname}! Чем сегодня займёмся?*☺️",
                         reply_markup=welcome.welcome_keyboard(),
                         parse_mode="Markdown")
