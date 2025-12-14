from logs import logger
import services.system_rules as sr
from services.chat_request import ChatLLM
from services.extract_json import extract_json
from services.fixer import CURRENCY_RATE
from services.exceptions import ServiceException
from services.weather import get_weather

def complex_service(
        countryFrom: str,
        countryTo: str | None = None,
        cityTo: str | None = None) -> dict[str, str | float]:
    logger.debug(f"complex_service countryFrom={countryFrom}, countryTo={countryTo}, cityTo={cityTo}")
    chat = ChatLLM(sr.SYSTEM_CONTENT).user_message(f"from {countryFrom}' to {countryTo or cityTo}")
    raw_response: str = chat.request()
    logger.debug(f"complex_service raw_response={raw_response}")
    json_data: dict | None = extract_json(raw_response)
    logger.debug(f"complex_service raw_response={raw_response}")
    
    if not json_data:
        raise ServiceException("Internal service error")
    
    json_data["weather_to"] = get_weather(cityTo or json_data[sr.capital_to])
    json_data["exchange_rate"] = CURRENCY_RATE.get_rate(json_data[sr.currency_from_code], json_data[sr.currency_to_code])
    
    return json_data