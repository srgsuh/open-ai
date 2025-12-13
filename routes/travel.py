from fastapi import APIRouter, Depends
from logs import logger
from models.TravelRequest import TravelRequest
from models.TravelResponse import TravelResponse
from services.complex_service import complex_service
from models.mappings import travel_response_mapper
from auth import get_current_user

travel_router = APIRouter()

@travel_router.post("/info", response_model=TravelResponse, response_model_exclude_none=True)
async def post_info(request: TravelRequest, user=Depends(get_current_user)) -> TravelResponse:
    logger.debug(f"post_info. Request: {request}, user={user}")
    data = complex_service(
        request.countryFrom,
        request.countryTo,
        request.isCapital == True,
        request.isWeather == True,
        request.isCurrency == True
    )
    return travel_response_mapper(data)

@travel_router.get("/info", response_model=TravelResponse, response_model_exclude_none=True)
async def get_info(countryFrom: str, countryTo: str) -> TravelResponse:
    logger.debug(f"get_info. countryFrom: {countryFrom}, countryTo: {countryTo}")
    data = complex_service(countryFrom, countryTo, True, True, True)
    return travel_response_mapper(data)