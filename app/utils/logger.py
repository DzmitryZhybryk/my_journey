from loguru import logger as _logger

__all__ = [
    "get_logger"
]


def configure_logger() -> None:
    _logger.add('logs/debug.log', format="{time} {level} {message}", level="DEBUG")
    _logger.add('logs/warning.log', format="{time} {level} {message}", level="WARNING")
    _logger.add('logs/error.log', format="{time} {level} {message}", level="ERROR")


def get_logger():
    return _logger
