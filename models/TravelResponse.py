from pydantic import BaseModel, Field

class TravelResponse(BaseModel):
    countryFrom: str
    countryTo: str
    capitalTo: str | None = None
    weatherTo: str | None = None
    currencyCodeFrom: str | None = Field(default=None, min_length=3, max_length=3)
    currencyCodeTo: str | None = Field(default=None, min_length=3, max_length=3)
    currencyNameFrom: str | None = None
    currencyNameTo: str | None = None
    exchangeRate: float | None = None