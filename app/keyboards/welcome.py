from aiogram.utils import keyboard

from app import schemas


def make_start() -> keyboard.InlineKeyboardMarkup:
    keyboard_builder = keyboard.InlineKeyboardBuilder()

    keyboard_builder.button(text="Памагити!", callback_data=schemas.WelcomeKeyboardSchema(help="help"))
    keyboard_builder.button(text="Регистрация",
                            callback_data=schemas.WelcomeKeyboardSchema(registration="registration"))
    keyboard_builder.button(text="Личный кабинет",
                            callback_data=schemas.WelcomeKeyboardSchema(personal="personal"))
    keyboard_builder.button(text="Путешествия", callback_data=schemas.WelcomeKeyboardSchema(add_travel="add_travel"))

    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
