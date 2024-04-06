
from aiogram import types

from app.keyboards.personal import get_reply_keyboard


async def personal_data(message: types.Message):
    await message.answer('What do you want to get?', reply_markup=get_reply_keyboard())
