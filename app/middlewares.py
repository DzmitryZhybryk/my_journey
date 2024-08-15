from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware, types

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


class ProtectionMiddleware(BaseMiddleware):
    PROTECTED_HANDLER = {
        "travel_callback",
        "add_travel_callback",
        "get_travel_callback",
        "get_all_travels_callback",
        "get_distance_callback",
        "get_country_callback",
        "delete_travel_callback",
        "set_nickname_callback",
        "delete_user_callback",
        "set_birthday_callback",
        "about_me_callback",
    }

    async def __call__(self,
                       handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
                       event: types.Message,  # type: ignore
                       data: dict[str, Any]) -> Any:
        handler_object = data.get("handler")
        handler_name = handler_object.callback.__name__ if handler_object else None

        if handler_name in self.PROTECTED_HANDLER:
            if event.from_user:
                user = await storage.get_user(user_id=event.from_user.id)
                if not user or user.is_active is False:
                    await event.answer(
                        text="Вы должны быть зарегистрированным пользователем для использования этого функционала",
                        show_alert=True
                    )
                    return None

        return await handler(event, data)
