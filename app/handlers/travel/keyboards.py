from aiogram.filters.callback_data import CallbackData
from aiogram.utils import keyboard


class TravelKeyboardSchema(CallbackData, prefix="travel"):
    add_travel: str | None = None
    get_travel: str | None = None
    delete_travel: str | None = None
    update_travel: str | None = None


def travel_keyboard() -> keyboard.InlineKeyboardMarkup:
    keyboard_builder = keyboard.InlineKeyboardBuilder()

    keyboard_builder.button(text="Добавить путешествие",
                            callback_data=TravelKeyboardSchema(add_travel="add_travel"))
    keyboard_builder.button(text="Получить информацию о имеющихся путешествиях",
                            callback_data=TravelKeyboardSchema(get_travel="get_travel"))
    keyboard_builder.button(text="Удалить путешествие",
                            callback_data=TravelKeyboardSchema(delete_travel="delete_travel"))
    keyboard_builder.button(text="Редактировать путешествие",
                            callback_data=TravelKeyboardSchema(update_travel="update_travel"))

    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
