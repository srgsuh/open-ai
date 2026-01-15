from .TravelResponse import TravelResponse
from services.complex_service import ComplexTravelData

def travel_response_mapper(data: ComplexTravelData) -> TravelResponse:
    return TravelResponse(
        countryFrom=data.country_from,
        countryTo=data.country_to,
        capitalTo=data.capital_to,
        weatherTo=data.weather_to,
        currencyCodeFrom=data.currency_from_code,
        currencyCodeTo=data.currency_to_code,
        currencyNameFrom=data.currency_from_name,
        currencyNameTo=data.currency_to_name,
        exchangeRate=data.exchange_rate
    )