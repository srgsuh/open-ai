from typing import Any
import requests
from configuration import get_api_key, get_url
from datetime import datetime

__placeholder: str = "unknown"
__empty_dict: dict[str, Any] = {}

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

def __parse_response(json_data: dict[str, Any]) -> dict[str, str]:
    location: dict[str, Any] = json_data.get("location", __empty_dict)
    current_weather: dict[str, Any] = json_data.get("current", __empty_dict)
    if not location or not current_weather:
        raise UnknownLocationError("Unknown city name")
    
    return {
        "city": location.get("name", ""),
        "temperature": current_weather.get("temp_c", ""),
        "condition": current_weather.get("condition", __empty_dict).get("text", ""),
        "humidity": current_weather.get("humidity", ""),
        "wind speed": current_weather.get("wind_kph", "")
    }

def __weather_data_to_str(data: dict[str, str]) -> str:
    today: str = datetime.now().strftime("%d.%m.%Y")
    city = data["city"]
    temperature = data["temperature"] if data["temperature"] is not None else __placeholder
    condition = data["condition"] if data["condition"] is not None else __placeholder
    humidity = data["humidity"] if data["humidity"] is not None else __placeholder
    wind_speed = data["wind speed"] if data["wind speed"] is not None else __placeholder
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
        weather_data: dict[str, str] = __parse_response(json_data)
        description = __weather_data_to_str(weather_data)
    except Exception as e:
        description = f"Weather forecast in {city_name} is unavailable. Error: {str(e)}"

    return description

if __name__ == "__main__":
    print(get_weather("11"))
    print(get_weather("oooooooooopsss"))