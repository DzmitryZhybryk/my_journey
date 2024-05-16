from aiogram.filters.callback_data import CallbackData


class ReturnKeyboardSchema(CallbackData, prefix="return"):
    to_welcome: str | None = None
    to_base_travel: str | None = None
