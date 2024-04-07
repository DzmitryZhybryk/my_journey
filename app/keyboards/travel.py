from aiogram.utils import keyboard

from app import schemas


def make_travel() -> keyboard.InlineKeyboardMarkup:
    keyboard_builder = keyboard.InlineKeyboardBuilder()

    keyboard_builder.button(text="Добавить путешествие", callback_data=schemas.TravelSchema(add_travel="add_travel"))
    keyboard_builder.button(text="Получить информацию о имеющихся путешествиях",
                            callback_data=schemas.TravelSchema(get_travels="get_travels"))

    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def make_language() -> keyboard.ReplyKeyboardMarkup:
    keyboard_builder = keyboard.ReplyKeyboardBuilder()

    keyboard_builder.button(text="ru")
    keyboard_builder.button(text="en")
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def make_transport_type() -> keyboard.ReplyKeyboardMarkup:
    keyboard_builder = keyboard.ReplyKeyboardBuilder()

    keyboard_builder.button(text="Воздушный")
    keyboard_builder.button(text="Наземный")
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
