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

def get_api_key() -> str:
    return get_config_parameter("API_KEY")

def get_url() -> str:
    return get_config_parameter("URL_CURRENT")