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

def __parse_response(data: dict[str, Any]) -> dict[str, str]:
    location: dict[str, Any] = data.get("location", __empty_dict)
    current_weather: dict[str, Any] = data.get("current", __empty_dict)
    if not location or not current_weather:
        raise UnknownLocationError("Unknown city name")
    
    return {
        "city": location.get("name", ""),
        "temperature": current_weather.get("temp_c", ""),
        "condition": current_weather.get("condition", __empty_dict).get("text", ""),
        "humidity": current_weather.get("humidity", ""),
        "wind speed": current_weather.get("wind_kph", "")
    }

