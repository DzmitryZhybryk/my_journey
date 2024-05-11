from aiogram import BaseMiddleware, types
from typing import Callable, Awaitable, Dict, Any

from app.database import storage


class SetNicknameMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
                       event: types.Message,  # type: ignore
                       data: dict[str, Any]) -> Any:
        if event.from_user:
            user = await storage.get_user(user_id=event.from_user.id)
            data["nickname"] = user.nickname if user else "Семпай"
        return await handler(event, data)
