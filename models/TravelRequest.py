from pydantic import BaseModel

class TravelRequest(BaseModel):
    countryFrom: str
    countryTo: str
    isCapital: bool
    isWeather: bool
    isCurrency: bool