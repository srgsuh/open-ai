from typing import Any
import requests
from configuration import get_api_key, get_url
from datetime import datetime

__placeholder: str = "unknown"
__empty_dict: dict[str, Any] = {}

#weather data dictionary keys:
__CITY: str = "city"
__TEMP: str = "temp"
__CONDITION: str = "condition"
__HUMIDITY: str = "humidity"
__WIND: str = "wind_speed"

class UnknownLocationError(RuntimeError):
    """City name not found"""

def __query_params(city_name: str) -> dict[str, str]:
    return {
        "key": get_api_key(),
        "q": city_name,
        "aqi": "no"
    }

def __get_api_response(city_name: str) -> dict[str, Any]:
    response = requests.get(get_url(), params=__query_params(city_name))
    response.raise_for_status()
    return response.json()

def __parse_response(json_data: dict[str, Any]) -> dict[str, str | None]:
    location: dict[str, Any] = json_data.get("location", __empty_dict)
    current_weather: dict[str, Any] = json_data.get("current", __empty_dict)
    if not location or not current_weather:
        raise UnknownLocationError("Unknown city name")
    
    return {
        __CITY: location.get("name"),
        __TEMP: current_weather.get("temp_c", __placeholder),
        __CONDITION: current_weather.get("condition", __empty_dict).get("text", __placeholder),
        __HUMIDITY: current_weather.get("humidity", __placeholder),
        __WIND: current_weather.get("wind_kph", __placeholder)
    }

def __weather_data_to_str(data: dict[str, str | None]) -> str:
    today: str = datetime.now().strftime("%d.%m.%Y")
    city = data[__CITY]
    temperature = data[__TEMP]
    condition = data[__CONDITION]
    humidity = data[__HUMIDITY]
    wind_speed = data[__WIND]
    return (
        f"Weather in {city} on {today}: "
        f"{temperature}°C, {condition}. "
        f"Humidity: {humidity}%, "
        f"Wind: {wind_speed} km/h."
    )

def get_weather(city_name: str) -> str:
    description: str = ""
    try:
        json_data: dict[str, Any] = __get_api_response(city_name)
        weather_data: dict[str, str | None] = __parse_response(json_data)
        description = __weather_data_to_str(weather_data)
    except Exception as e:
        description = f"Weather forecast in {city_name} is unavailable. Error: {str(e)}"

    return description

if __name__ == "__main__":
    print(get_weather("Los Angeles"))