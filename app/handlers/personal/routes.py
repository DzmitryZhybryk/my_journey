import datetime

from aiogram import types, Router, Bot, F
from aiogram.fsm.context import FSMContext

from app.config import settings
from app.database import storage
from app.handlers.personal import stateforms
from app.handlers import personal

router = Router()


@router.callback_query(F.data == "personal:set_nickname::::")
async def set_nickname_callback(callback: types.CallbackQuery, bot: Bot, state: FSMContext) -> None:
    text = "Обращаю внимание, что бот будет использовать его для обращения к вам. Просьба соблюдать приличие😏"
    await callback.answer(text=text,
                          show_alert=True)
    await bot.send_message(chat_id=callback.from_user.id,
                           text="Какой никнейм хотите задать?")
    await state.set_state(stateforms.SetNickname.NICKNAME)


@router.message(stateforms.SetNickname.NICKNAME)
async def set_nickname(message: types.Message, bot: Bot) -> None:
    nickname = message.text
    if message.from_user and nickname:
        await storage.update_user(user_id=message.from_user.id, nickname=nickname)
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Никнейм {nickname} успешно добавлен")


@router.callback_query(F.data == "personal::set_birthday:::")
async def set_birthday_callback(callback: types.CallbackQuery, bot: Bot, state: FSMContext) -> None:
    await callback.answer("Давайте зададим дату рождения")
    await bot.send_message(chat_id=callback.from_user.id,
                           text="Какую дату рождения вы хотите задать? Пожалуйста, используйте формат дд-мм-гггг")
    await state.set_state(stateforms.SetBirthday.BIRTHDAY)


@router.message(stateforms.SetBirthday.BIRTHDAY)
async def set_birthday(message: types.Message, bot: Bot) -> None:
    if message.text:
        birthday_date = datetime.datetime.strptime(message.text, "%d-%m-%Y").date()
        if birthday_date > datetime.date.today():
            await message.answer(
                text="Вы пытаетесь установить дату рождения из будущего. Интригующе, но маловероятно😉")
            return None

        if message.from_user:
            await storage.update_user(user_id=message.from_user.id, birthday=birthday_date)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"Ваш день рождения {message.text} добавлен")


@router.callback_query(F.data == "personal:::about_me::")
async def about_me_callback(callback: types.CallbackQuery, bot: Bot) -> None:
    await callback.answer(text="Что именно вас интересует?")
    await bot.send_message(chat_id=callback.from_user.id,
                           text="Что именно вас интересует?",
                           reply_markup=personal.about_me_keyboard())


@router.callback_query(F.data == "personal::::delete_user:")
async def delete_user_callback(callback: types.CallbackQuery, bot: Bot, state: FSMContext) -> None:
    await callback.answer(text="Удаляем пользователя. Будьте внимательны!",
                          show_alert=True)
    await bot.send_message(chat_id=callback.from_user.id,
                           text="Вы действительно хотите удалить свой профиль? Ответьте 'да', если это так")
    await state.set_state(stateforms.DeleteUser.DELETE)


@router.message(stateforms.DeleteUser.DELETE)
async def delete_user(message: types.Message, bot: Bot) -> None:
    if message.text and message.text.lower() == "да" and message.from_user:
        await storage.update_user(user_id=message.from_user.id,
                                  deleted_date=datetime.datetime.now(tz=datetime.timezone.utc))
        photo = types.FSInputFile(settings.STATIC_STORAGE / "sadness.webp")
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=photo,
                             caption="Мы будем скучать🥲")


@router.callback_query(F.data == "personal:::::restore_user")
async def restore_user_callback(callback: types.CallbackQuery, bot: Bot) -> None:
    await callback.answer(text="Мы ради, что Вы вернулись! Восстанавливаем пользователя",
                          show_alert=True)
    await storage.update_user(user_id=callback.from_user.id, deleted_date=None)
    photo = types.FSInputFile(settings.STATIC_STORAGE / "happy.webp")
    await bot.send_photo(chat_id=callback.from_user.id,
                         photo=photo,
                         caption="Ваш профиль успешно восстановлен")
