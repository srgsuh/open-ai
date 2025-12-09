import sys
from loguru import logger
from configuration import get_config_parameter

FILE_DEBUG_LEVEL: str = get_config_parameter("FILE_DEBUG_LEVEL", "")
CONSOLE_DEBUG_LEVEL: str = get_config_parameter("CONSOLE_DEBUG_LEVEL", "")

LOG_FORMAT: str = "{time:HH:mm:ss}: {message}"

logger.remove()
try:
    if FILE_DEBUG_LEVEL:
        logger.add("./logs/file_{time:YYYY_MM_DD_HH_mm_ss}.log", format=LOG_FORMAT, level=FILE_DEBUG_LEVEL)
    if CONSOLE_DEBUG_LEVEL:
        logger.add(sys.stdout, format=LOG_FORMAT, level=CONSOLE_DEBUG_LEVEL)
except Exception as e:
    print(f"Logger config error: {str(e)}. Starting application without logging.")

__all__ = ["logger"]