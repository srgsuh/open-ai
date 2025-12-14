from typing import Self
from pydantic import BaseModel, model_validator

class TravelRequest(BaseModel):
    countryFrom: str
    countryTo: str | None = None
    cityTo: str | None = None
    isCapital: bool | None = None
    isWeather: bool | None = None
    isCurrency: bool | None = None

    @model_validator(mode="after")
    def validate_destination(self) -> Self:
        if bool(self.countryTo) == bool(self.cityTo):
            raise ValueError('Exactly one of the fields "countryTo", "cityTo" must be provided')
        if bool(self.isCapital) and not bool(self.countryTo):
            raise ValueError('Field "isCapital" can only be provided with the field "countryTo"')

        return self
    
    def whereTo(self) -> str:
        return self.countryTo or self.cityTo or ""