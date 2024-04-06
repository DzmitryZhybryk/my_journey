from aiogram.utils import keyboard


def about_me() -> keyboard.ReplyKeyboardMarkup:
    keyboard_builder = keyboard.ReplyKeyboardBuilder()
    keyboard_builder.button(text="Локация", request_location=True)
    keyboard_builder.button(text="Контакт", request_contact=True)
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(resize_keyboard=True,
                                      one_time_keyboard=True,
                                      input_field_placeholder='Send location or phone number')  # TODO шо это
