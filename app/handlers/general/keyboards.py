from aiogram.filters.callback_data import CallbackData


class ReturnKeyboardSchema(CallbackData, prefix="return"):
    to_welcome: str | None = None
