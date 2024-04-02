from aiogram.filters.callback_data import CallbackData
from pydantic import BaseModel


class WelcomeSchema(CallbackData, prefix="welcome"):
    help: str | None = None
    about_me: str | None = None
    add_travel: str | None = None


class AllCommandSchema(BaseModel):
    start: str = "Начать работу с ботом"
    help: str = "Памагити!"
