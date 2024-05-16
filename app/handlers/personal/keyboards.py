from aiogram.filters.callback_data import CallbackData
from aiogram.utils import keyboard

from app.handlers import general


class PersonalAreaKeyboardSchema(CallbackData, prefix="personal"):
    set_nickname: str | None = None
    set_birthday: str | None = None
    about_me: str | None = None
    delete_user: str | None = None
    restore_user: str | None = None


def personal_keyboard() -> keyboard.InlineKeyboardMarkup:
    keyboard_builder = keyboard.InlineKeyboardBuilder()

    keyboard_builder.button(text="Добавить никнейм",
                            callback_data=PersonalAreaKeyboardSchema(set_nickname="set_nickname"))
    keyboard_builder.button(text="Добавить дату рождения",
                            callback_data=PersonalAreaKeyboardSchema(set_birthday="set_birthday"))
    keyboard_builder.button(text="Получить свою геолокацию/контакт",
                            callback_data=PersonalAreaKeyboardSchema(about_me="about_me"))
    keyboard_builder.button(text="Удалить профиль",
                            callback_data=PersonalAreaKeyboardSchema(delete_user="delete_user"))
    keyboard_builder.button(text="Восстановить профиль",
                            callback_data=PersonalAreaKeyboardSchema(restore_user="restore_user"))
    keyboard_builder.button(text="Назад",
                            callback_data=general.ReturnKeyboardSchema(to_welcome="to_welcome"))

    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def about_me_keyboard() -> keyboard.ReplyKeyboardMarkup:
    keyboard_builder = keyboard.ReplyKeyboardBuilder()
    keyboard_builder.button(text="Локация", request_location=True)
    keyboard_builder.button(text="Контакт", request_contact=True)
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(resize_keyboard=True,
                                      one_time_keyboard=True,
                                      input_field_placeholder='Send location or phone number')  # TODO шо это
