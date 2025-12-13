from configuration import get_config_parameter
import jwt

def get_secret_key() -> str:
    return get_config_parameter("SECRET_KEY")
