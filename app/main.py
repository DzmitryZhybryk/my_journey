import asyncio

from aiogram import Bot, Dispatcher

from app import middlewares
from app.commands import set_commands
from app.config import settings
from app.handlers.admin.routes import router as admin_router
from app.handlers.general.routes import router as general_router
from app.handlers.personal.routes import router as personal_router
from app.handlers.travel.routes import router as travel_router
from app.handlers.welcome.routes import router as welcome_router
from app.utils.logger import get_logger

logger = get_logger()


async def start_bot(bot: Bot) -> None:
    await set_commands(bot=bot)
    logger.warning(f"Начало работы бота {settings.RUN_MODE}")


async def stop_bot(bot: Bot) -> None:
    logger.warning("Бот остановлен!")


def register_routers(dp: Dispatcher) -> None:
    dp.include_router(welcome_router)
    dp.include_router(personal_router)
    dp.include_router(travel_router)
    dp.include_router(general_router)
    dp.include_router(admin_router)


async def main() -> None:
    bot: Bot = Bot(token=settings.dump_secret(settings.TELEGRAM_BOT_API_TOKEN))
    dp: Dispatcher = Dispatcher()

    register_routers(dp)

    dp.message.middleware(middlewares.SetNicknameMiddleware())
    dp.callback_query.middleware(middlewares.SetNicknameMiddleware())
    dp.message.middleware(middlewares.ProtectionMiddleware())
    dp.callback_query.middleware(middlewares.ProtectionMiddleware())

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    try:
        await dp.start_polling(bot, skip_updates=False)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
