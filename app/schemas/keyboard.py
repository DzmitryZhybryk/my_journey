from aiogram.filters.callback_data import CallbackData


class GetTravelKeyboardSchema(CallbackData, prefix="my_travel"):
    get_travel: str | None = None
    get_distance: str | None = None
    get_country: str | None = None
