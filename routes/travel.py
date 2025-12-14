from fastapi import APIRouter, Depends
from logs import logger
from models.TravelRequest import TravelRequest
from models.TravelResponse import TravelResponse
from services.complex_service import complex_service
from models.mappings import travel_response_mapper
from users import collect_user_statistics

travel_router = APIRouter(dependencies=[Depends(collect_user_statistics)])

@travel_router.post("/info", response_model=TravelResponse, response_model_exclude_none=True)
async def post_info(request: TravelRequest) -> TravelResponse:
    logger.debug(f"post_info. Request: {request}")
    data = complex_service(
        countryFrom=request.countryFrom,
        countryTo=request.countryTo,
        cityTo=request.cityTo,
    )
    return travel_response_mapper(data, request.cityTo, bool(request.isCapital), bool(request.isWeather), bool(request.isCurrency))

@travel_router.get("/info", response_model=TravelResponse, response_model_exclude_none=True)
async def get_info(countryFrom: str, countryTo: str) -> TravelResponse:
    logger.debug(f"get_info. countryFrom: {countryFrom}, countryTo: {countryTo}")
    data = complex_service(countryFrom, countryTo)
    return travel_response_mapper(data)