
from loguru import logger

logger.add('logs/debug.log', format="{time} {level} {message}", level="DEBUG")
logger.add('logs/warning.log', format="{time} {level} {message}", level="WARNING")
logger.add('logs/error.log', format="{time} {level} {message}", level="ERROR")
