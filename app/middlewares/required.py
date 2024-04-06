from aiogram import BaseMiddleware, types
from typing import Callable, Awaitable, Dict, Any

from app.config import settings


class RequiredMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
                       event: types.Message,
                       data: dict[str, Any]) -> Any:
        print(event.from_user.id)
        # if event.from_user.id == config.MY_TELEGRAM_ID:
        #     return await handler(event, data)
        #
        # await event.answer(config.GREETING_STRANGERS)