from pydantic import BaseModel

class TravelRequest(BaseModel):
    countryFrom: str
    countryTo: str
    isCapital: bool | None = None
    isWeather: bool | None = None
    isCurrency: bool | None = None