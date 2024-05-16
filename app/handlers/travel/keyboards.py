from aiogram.filters.callback_data import CallbackData
from aiogram.utils import keyboard

from app.handlers import general


class TravelKeyboardSchema(CallbackData, prefix="travel"):
    add_travel: str | None = None
    get_travel: str | None = None
    delete_travel: str | None = None


def travel_keyboard() -> keyboard.InlineKeyboardMarkup:
    keyboard_builder = keyboard.InlineKeyboardBuilder()

    keyboard_builder.button(text="Добавить путешествие",
                            callback_data=TravelKeyboardSchema(add_travel="add_travel"))
    keyboard_builder.button(text="Получить информацию о имеющихся путешествиях",
                            callback_data=TravelKeyboardSchema(get_travel="get_travel"))
    keyboard_builder.button(text="Удалить путешествие",
                            callback_data=TravelKeyboardSchema(delete_travel="delete_travel"))
    keyboard_builder.button(text="Назад",
                            callback_data=general.ReturnKeyboardSchema(to_welcome="to_welcome"))

    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def transport_type_keyboard() -> keyboard.ReplyKeyboardMarkup:
    keyboard_builder = keyboard.ReplyKeyboardBuilder()

    keyboard_builder.button(text="Воздушный")
    keyboard_builder.button(text="Наземный")

    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


class GetTravelKeyboardSchema(CallbackData, prefix="my_travel"):
    get_travel: str | None = None
    get_distance: str | None = None
    get_country: str | None = None
    get_detail: str | None = None


def get_travel_keyboard() -> keyboard.InlineKeyboardMarkup:
    keyboard_builder = keyboard.InlineKeyboardBuilder()

    keyboard_builder.button(text="Посмотреть все путешествия",
                            callback_data=GetTravelKeyboardSchema(get_travel="get_travel"))
    keyboard_builder.button(text="Оценить дистанцию",
                            callback_data=GetTravelKeyboardSchema(get_distance="get_distance"))
    keyboard_builder.button(text="Информация по странам",
                            callback_data=GetTravelKeyboardSchema(get_country="get_country"))
    keyboard_builder.button(text="Получить подробную информацию",
                            callback_data=GetTravelKeyboardSchema(get_detail="get_detail"))
    keyboard_builder.button(text="Назад",
                            callback_data=general.ReturnKeyboardSchema(to_base_travel="to_base_travel"))

    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def one_more_travel_keyboard() -> keyboard.InlineKeyboardMarkup:
    keyboard_builder = keyboard.InlineKeyboardBuilder()

    keyboard_builder.button(text="Да",
                            callback_data=TravelKeyboardSchema(add_travel="add_travel"))
    keyboard_builder.button(text="Нет",
                            callback_data=general.ReturnKeyboardSchema(to_base_travel="to_base_travel"))

    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
