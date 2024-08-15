from aiogram import types, Router, Bot, F
from aiogram.fsm.context import FSMContext

from app.database import storage
from app.handlers import admin
from app.models import RoleEnum
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
async def change_user_role_callback(callback: types.CallbackQuery, bot: Bot, state: FSMContext) -> None:
    await callback.answer("Изменение роли пользователя")
    await bot.send_message(chat_id=callback.from_user.id,
                           text="Введите ID пользователя, которому хотите изменить роль")
    await state.set_state(admin.ChangeRole.UserID)


@router.message(admin.ChangeRole.UserID)
async def get_user_id(message: types.Message, state: FSMContext) -> None:
    user_id = message.text
    await message.answer(f"Изменение роли для пользователя с id: *{user_id}*. Какую роль хотите назначить?",
                         parse_mode="Markdown",
                         reply_markup=admin.user_role_keyboard())
    await state.update_data(user_id=user_id)
    await state.set_state(admin.ChangeRole.ROLE)


@router.message(admin.ChangeRole.ROLE)
async def get_new_role(message: types.Message, state: FSMContext) -> None:
    role = message.text
    if role not in RoleEnum.get_roles():
        await message.answer(text=f"Роли {role} не существует")
        return

    await state.update_data(role=role)
    await state.set_state(admin.ChangeRole.ROLE)

    update_data = admin.ChangeUserRoleSchema(**await state.get_data())

    user = await storage.get_user(user_id=update_data.user_id)
    if not user:
        await message.answer(text=f"Пользователь с ID {update_data.user_id} не найден")
        await state.clear()
        return

    await storage.update_user(user_id=update_data.user_id, role=update_data.role)
    await message.answer(text=f"Установлена новая роль *{role}* для пользователя с ID *{update_data.user_id}*",
                         parse_mode="Markdown")
    await state.clear()
