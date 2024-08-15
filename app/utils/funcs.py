from aiogram import Bot

from app.config import settings


async def send_long_message(chat_id: int, text: str, bot: Bot, parse_mode: str) -> None:
    for i in range(0, len(text), settings.MAX_MESSAGE_LENGTH):
        await bot.send_message(chat_id=chat_id,
                               text=text[i:i + settings.MAX_MESSAGE_LENGTH],
                               parse_mode=parse_mode)
