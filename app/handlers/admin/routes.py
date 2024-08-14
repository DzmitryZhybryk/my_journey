from aiogram import types, Router, Bot, F

from app.database import storage
from app.utils import funcs

router = Router()


@router.callback_query(F.data == "admin:get_active_users:")
async def get_active_users(callback: types.CallbackQuery, bot: Bot) -> None:
    await callback.answer(text="Получение всех пользователей")
    users = await storage.get_all_users(is_active=True)

    if not users:
        await bot.send_message(chat_id=callback.from_user.id,
                               text="No users found.")
        return

    response = "\n\n".join(
        f"*ID:* {user.telegram_id}\n"
        f"*Full Name:* {user.full_name}\n"
        f"*Username:* {user.username}\n"
        f"*Nickname:* {user.nickname}\n"
        f"*Role:* {user.role}\n"
        f"*Active:* {user.is_active}"
        for user in users
    )

    await funcs.send_long_message(chat_id=callback.from_user.id,
                                  text=response,
                                  bot=bot,
                                  parse_mode="Markdown")


@router.callback_query(F.data == "admin::change_user_role")
async def change_user_role(callback: types.CallbackQuery, bot: Bot) -> None:
    text = "Обращаю внимание!"
    await callback.answer(text=text,
                          show_alert=True)
    await bot.send_message(chat_id=callback.from_user.id,
                           text="Какой никнейм хотите задать?")
