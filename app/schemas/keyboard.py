from aiogram.filters.callback_data import CallbackData
from pydantic import BaseModel


class AllCommandSchema(BaseModel):
    help: str = "Памагити!"
    start: str = "Начать работу с ботом"
    about_me: str = "Получить персональные данные"
    cancel: str = "Отменить все и вернуться к началу"


class WelcomeSchema(CallbackData, prefix="welcome"):
    help: str | None = None
    about_me: str | None = None
    add_travel: str | None = None


class TravelSchema(CallbackData, prefix="travel"):
    add_travel: str | None = None
    get_travels: str | None = None
