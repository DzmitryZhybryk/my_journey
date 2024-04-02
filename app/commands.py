from aiogram import Bot, types


async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(
            command="start",
            description="Beginning of work"
        ),
        types.BotCommand(
            command="my_data",
            description="My personal data"
        ),
        # types.BotCommand(
        #     command="load",
        #     description="Load you travel info"
        # ),
        # types.BotCommand(
        #     command="cancel",
        #     description="Cancel all"
        # ),
        # types.BotCommand(
        #     command="get_trips",
        #     description="Get all trip data"
        # ),
        # types.BotCommand(
        #     command="registrate",
        #     description="Registrate new user"
        # )
    ]

    await bot.set_my_commands(commands, types.BotCommandScopeDefault())
