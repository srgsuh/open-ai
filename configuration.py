from dotenv import load_dotenv
import os
from logs import logger

load_dotenv()

class ConfigurationError(RuntimeError):
    pass

def get_config_parameter(parameter_name: str, default_value: str | None = None) -> str:
    parameter: str | None = os.getenv(parameter_name, default=default_value)
    logger.debug("The value of the parameter \"%s\"=\"%s\"", parameter_name, parameter)
    if parameter is None:
        raise ConfigurationError(f"Missing configuration for the parameter: {parameter_name}")
    return parameter