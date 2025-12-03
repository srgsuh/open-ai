from loguru import logger
from configuration import get_config_parameter

DEBUG_ON: str = get_config_parameter("DEBUG_ON", "")

if DEBUG_ON:
    logger.remove()
    logger.add("./logs/file_{time:YYYY_MM_DD_HH_mm_ss}.log", format="{time:HH:mm:ss}: {message}", level="DEBUG")

def debug(message: str) -> None:
    if DEBUG_ON:
        logger.debug(message)