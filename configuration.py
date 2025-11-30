from dotenv import load_dotenv
import os

load_dotenv()

class ConfigurationError(RuntimeError):
    pass

def get_config_parameter(parameter_name: str) -> str:
    parameter = os.getenv(parameter_name)
    if parameter is None:
        raise ConfigurationError(f"Missing configuration for the parameter: {parameter_name}")
    return parameter

API_KEY: str = get_config_parameter("API_KEY")
URL_CURRENT = get_config_parameter("URL_CURRENT")