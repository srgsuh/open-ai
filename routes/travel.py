from fastapi import APIRouter, Depends
from logs import get_logger
from models.TravelRequest import TravelRequest
from models.TravelResponse import TravelResponse
from services.complex_service import complex_service
from models.mappings import travel_response_mapper
from auth import get_user_token, get_admin_token

logger = get_logger("travel")

travel_router = APIRouter()

@travel_router.post("/travel", response_model=TravelResponse, response_model_exclude_none=True)
async def post_info(request: TravelRequest, user_data: dict = Depends(get_user_token)) -> TravelResponse:
    logger.debug(f"post_info. Request: {request}")
    logger.debug(f"post_info. User: {user_data}")
    data = complex_service(
        request.countryFrom,
        request.countryTo,
        request.isCapital == True,
        request.isWeather == True,
        request.isCurrency == True
    )
    response = travel_response_mapper(data)
    logger.debug(f"post_info. Response: {response}")
    return response

@travel_router.get("/travel", response_model=TravelResponse, response_model_exclude_none=True)
async def get_info(request: TravelRequest = Depends(), user_data: dict = Depends(get_admin_token)) -> TravelResponse:
    logger.debug(f"get_info. Request: {request}")
    logger.debug(f"get_info. User: {user_data}")
    data = complex_service(request.countryFrom, request.countryTo, True, True, True)
    response = travel_response_mapper(data)
    logger.debug(f"get_info. Response: {response}")

    return response