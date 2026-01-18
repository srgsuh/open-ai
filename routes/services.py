from typing import Optional
from fastapi import APIRouter
from services.exchange_rates import get_exchange_rate_data
from services.weather import get_weather

services_router: APIRouter = APIRouter()

@services_router.get("/hello")
async def process_hello(name: Optional[str] = None) -> dict:
    return {
        "status": "OK",
        "greeting": f"Hello, {name if name is not None else "Anonymous"}"
    }

@services_router.get("/weather")
async def weather_process(city: str) -> dict:
    """
    Retrieve weather information for the specified city.
    """
    weather_info = get_weather(city)
    return {
        "status": "OK",
        "city": city,
        "weather": weather_info
    }

@services_router.get("/currency")
async def process_currency(currency_from: str, currency_to: str, full_names: bool = False) -> dict:
    """
    Get the exchange rate between two currencies.
    """
    exchange_info = get_exchange_rate_data(currency_from, currency_to, full_names)
    return {
        "status": "OK",
        "exchange_info": exchange_info
    }

@services_router.post("/mirror")
async def process_mirror(body: dict) -> dict:
    """
    Mirror the input JSON body back to the caller.
    """
    return {
        "status": "OK",
        "mirrored_body": body
    }