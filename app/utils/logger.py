from loguru import logger

__all__ = [
    "get_logger"
]


def configure_logger() -> None:
    logger.add('logs/debug.log', format="{time} {level} {message}", level="DEBUG")
    logger.add('logs/warning.log', format="{time} {level} {message}", level="WARNING")
    logger.add('logs/error.log', format="{time} {level} {message}", level="ERROR")


def get_logger() -> logger:  # type: ignore
    return logger
