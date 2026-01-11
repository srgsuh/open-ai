from logs import logger
import services.system_rules as sr
from services.chat_request import ChatLLM
from services.extract_json import extract_json
from services.exchange_rates import get_exchange_rate
from services.exceptions import ServiceException
from services.weather import get_weather
from dataclasses import dataclass

@dataclass
class ComplexTravelData:
    country_from: str
    currency_from_code: str | None
    currency_from_name: str | None
    country_to: str
    currency_to_code: str | None
    currency_to_name: str | None
    capital_to: str | None
    weather_to: str | None
    exchange_rate: float | None

_chat: ChatLLM
def get_chat() -> ChatLLM:
    global _chat
    if not _chat:
        _chat = ChatLLM(sr.SYSTEM_CONTENT)
    return _chat

def complex_service(
        countryFrom: str,
        countryTo: str,
        isCapital: bool = False,
        isWeather: bool = False,
        isCurrency: bool = False) -> ComplexTravelData:
    logger.debug(f"complex_service countryFrom={countryFrom}, countryTo={countryTo}, isCapital={isCapital}, isWeather={isWeather}, isCurrency={isCurrency}")
    chat = get_chat().user_message(f"from {countryFrom}' to {countryTo}")
    raw_response: str = chat.request()
    logger.debug(f"complex_service raw_response={raw_response}")
    json_data: dict | None = extract_json(raw_response)
    logger.debug(f"complex_service raw_response={raw_response}")
    
    if not json_data:
        raise ServiceException("Internal service error")
    
    return ComplexTravelData(
        country_from=json_data[sr.country_from],
        currency_from_code=json_data[sr.currency_from_code] if isCurrency else None,
        currency_from_name=json_data[sr.currency_from_name] if isCurrency else None,
        country_to=json_data[sr.country_to],
        currency_to_code=json_data[sr.currency_to_code] if isCurrency else None,
        currency_to_name=json_data[sr.currency_to_name] if isCurrency else None,
        capital_to=json_data[sr.capital_to] if isCapital else None,
        weather_to=get_weather(json_data[sr.capital_to]) if isWeather else None,
        exchange_rate=get_exchange_rate(json_data[sr.currency_from_code], json_data[sr.currency_to_code]) if isCurrency else None
    )