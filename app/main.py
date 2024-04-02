import asyncio

from app.commands import set_commands
from app.utils.logger import logger

from aiogram import Bot, Dispatcher

from app.config import settings
from app.handlers.base import router as base_router


async def start_bot(bot: Bot):
    await set_commands(bot=bot)
    logger.warning(f"Начало работы бота {settings.RUN_MODE}")


async def stop_bot(bot: Bot):
    logger.warning("Бот остановлен!")


def register_routers(dp: Dispatcher) -> None:
    dp.include_router(base_router)


async def main():
    bot: Bot = Bot(token=settings.dump_secret(settings.TELEGRAM_BOT_API_TOKEN), parse_mode='HTML')
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
