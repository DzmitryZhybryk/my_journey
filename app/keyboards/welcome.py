from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from app.keyboards.schemas import WelcomeSchema


def get_welcome_keyboard():
    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.button(text="Памагити!", callback_data=WelcomeSchema(help="help"))
    keyboard_builder.button(text="Получить личную информацию", callback_data=WelcomeSchema(about_me='about_me'))
    keyboard_builder.button(text="Добавим новое путешествие?", callback_data=WelcomeSchema(help='add_travel'))

    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_about_me_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="Локация", request_location=True)
    keyboard_builder.button(text="Контакт", request_contact=True)
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(resize_keyboard=True,
                                      one_time_keyboard=True,
                                      input_field_placeholder='Send location or phone number') # TODO шо это


def get_start_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="/start")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
