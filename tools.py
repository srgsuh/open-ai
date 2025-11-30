from typing import Any
import requests
from configuration import API_KEY, URL_CURRENT
from datetime import datetime

__placeholder: str = "unknown"
__empty_dict: dict[str, Any] = {}

class UnknownLocationError(RuntimeError):
    """City name not found"""

def __query_params(city_name: str) -> dict[str, str]:
    return {
        "key": API_KEY,
        "q": city_name,
        "aqi": "no"
    }

def __get_api_response(city_name: str) -> dict[str, Any]:
    response = requests.get(URL_CURRENT, params=__query_params(city_name))
    response.raise_for_status()
    return response.json()

