from aiogram import types, Router, Bot, F
from aiogram.filters import Command

from app import keyboards

router = Router()


@router.message(Command('about_me'))
async def about_me(message: types.Message) -> None:
    await message.answer(text="Что именно вас интересует?", reply_markup=keyboards.make_about_me())


@router.callback_query(F.data == "welcome::about_me:")
async def about_me_callback(callback: types.CallbackQuery, bot: Bot) -> None:
    await callback.answer("Что именно вас интересует?")
    await bot.send_message(chat_id=callback.from_user.id,
                           text="Что именно вас интересует?",
                           reply_markup=keyboards.make_about_me())
