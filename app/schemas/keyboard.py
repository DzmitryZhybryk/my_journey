from aiogram.filters.callback_data import CallbackData
from pydantic import BaseModel


class AllCommandSchema(BaseModel):
    help: str = "Памагити!"
    start: str = "Начать работу с ботом"
    cancel: str = "Отменить все и вернуться к началу"


class WelcomeKeyboardSchema(CallbackData, prefix="welcome"):
    help: str | None = None
    personal: str | None = None
    add_travel: str | None = None
    registration: str | None = None


class TravelKeyboardSchema(CallbackData, prefix="travel"):
    add_travel: str | None = None
    get_travel: str | None = None
    delete_travel: str | None = None
    update_travel: str | None = None


class GetTravelKeyboardSchema(CallbackData, prefix="my_travel"):
    get_travel: str | None = None
    get_distance: str | None = None
    get_country: str | None = None
