import asyncio

from app.commands import set_commands
from app.utils.logger import get_logger

from aiogram import Bot, Dispatcher

from app.config import settings
from app.handlers.welcome.routes import router as welcome_router
from app.handlers.personal.routes import router as personal_router
# from app.handlers.travel import router as travel_router

logger = get_logger()


async def start_bot(bot: Bot) -> None:
    await set_commands(bot=bot)
    logger.warning(f"Начало работы бота {settings.RUN_MODE}")


async def stop_bot(bot: Bot) -> None:
    logger.warning("Бот остановлен!")


def register_routers(dp: Dispatcher) -> None:
    dp.include_router(welcome_router)
    dp.include_router(personal_router)
    # dp.include_router(travel_router)


async def main() -> None:
    bot: Bot = Bot(token=settings.dump_secret(settings.TELEGRAM_BOT_API_TOKEN))
    dp: Dispatcher = Dispatcher()
    register_routers(dp)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    try:
        await dp.start_polling(bot, skip_updates=False)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
