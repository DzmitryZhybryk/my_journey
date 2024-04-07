from aiogram.utils import keyboard

from app import schemas


def make_start() -> keyboard.InlineKeyboardMarkup:
    keyboard_builder = keyboard.InlineKeyboardBuilder()

    keyboard_builder.button(text="Памагити!", callback_data=schemas.WelcomeSchema(help="help"))
    keyboard_builder.button(text="Получить личную информацию", callback_data=schemas.WelcomeSchema(about_me="about_me"))
    keyboard_builder.button(text="Путешествия", callback_data=schemas.WelcomeSchema(help="travel"))

    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
