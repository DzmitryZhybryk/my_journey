from aiogram.filters.callback_data import CallbackData
from aiogram.utils import keyboard


class WelcomeKeyboardSchema(CallbackData, prefix="welcome"):
    help: str | None = None
    registration: str | None = None
    personal: str | None = None
    travel: str | None = None
    admin: str | None = None


def welcome_keyboard() -> keyboard.InlineKeyboardMarkup:
    keyboard_builder = keyboard.InlineKeyboardBuilder()

    keyboard_builder.button(text="Памагити!",
                            callback_data=WelcomeKeyboardSchema(help="help"))
    keyboard_builder.button(text="Регистрация",
                            callback_data=WelcomeKeyboardSchema(registration="registration"))
    keyboard_builder.button(text="Личный кабинет",
                            callback_data=WelcomeKeyboardSchema(personal="personal"))
    keyboard_builder.button(text="Путешествия",
                            callback_data=WelcomeKeyboardSchema(travel="travel"))
    keyboard_builder.button(text="Админка",
                            callback_data=WelcomeKeyboardSchema(admin="admin"))

    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
