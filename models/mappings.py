from .TravelResponse import TravelResponse

def travel_response_mapper(
        data: dict,
        cityTo: str | None = None,
        isCapital: bool = True,
        isWeather: bool = True,
        isCurrency: bool = True
) -> TravelResponse:
    return TravelResponse(
        countryFrom=data["country_from"],
        countryTo=data["country_to"],
        cityTo=cityTo,
        capitalTo=data["capital_to"] if isCapital else None,
        weatherTo=data["weather_to"] if isWeather else None,
        currencyCodeFrom=data["currency_from_code"] if isCurrency else None,
        currencyCodeTo=data["currency_to_code"] if isCurrency else None,
        currencyNameFrom=data["currency_from_name"] if isCurrency else None,
        currencyNameTo=data["currency_to_name"] if isCurrency else None,
        exchangeRate=data["exchange_rate"] if isCurrency else None
    )