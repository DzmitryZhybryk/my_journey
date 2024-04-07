from aiogram import Bot, types


async def set_commands(bot: Bot) -> None:
    commands = [
        types.BotCommand(
            command="help",
            description="Памагити!"
        ),
        types.BotCommand(
            command="start",
            description="Начало работы с ботом"
        ),
        types.BotCommand(
            command="about_me",
            description="Получить персональные данные"
        ),
        types.BotCommand(
            command="cancel",
            description="Отменить все и вернуться к началу"
        ),
    ]
    await bot.set_my_commands(commands, types.BotCommandScopeDefault())
