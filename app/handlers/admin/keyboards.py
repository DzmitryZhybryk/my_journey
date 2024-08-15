from aiogram.filters.callback_data import CallbackData
from aiogram.utils import keyboard

from app.handlers import general
from app.models import RoleEnum


class AdminKeyboardSchema(CallbackData, prefix="admin"):
    get_active_users: str | None = None
    change_user_role: str | None = None


def admin_keyboard() -> keyboard.InlineKeyboardMarkup:
    keyboard_builder = keyboard.InlineKeyboardBuilder()

    keyboard_builder.button(text="Получить всех активных пользователей",
                            callback_data=AdminKeyboardSchema(get_active_users="get_active_users"))
    keyboard_builder.button(text="Изменить роль пользователя",
                            callback_data=AdminKeyboardSchema(change_user_role="change_user_role"))
    keyboard_builder.button(text="Назад",
                            callback_data=general.ReturnKeyboardSchema(to_welcome="to_welcome"))

    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def user_role_keyboard() -> keyboard.ReplyKeyboardMarkup:
    keyboard_builder = keyboard.ReplyKeyboardBuilder()

    [keyboard_builder.button(text=value) for value in RoleEnum.get_roles()]

    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
