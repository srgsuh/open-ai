from fastapi import APIRouter, Depends
from logs import get_logger
from models.TravelRequest import TravelRequest
from models.TravelResponse import TravelResponse
from services.complex_service import complex_service
from models.mappings import travel_response_mapper
from auth.auth import get_current_user, get_current_admin_user

logger = get_logger("travel")

travel_router = APIRouter()

@travel_router.post("/", response_model=TravelResponse, response_model_exclude_none=True)
async def post_info(request: TravelRequest, user_data = Depends(get_current_user)) -> TravelResponse:
    logger.debug(f"post_info. Request: {request}")
    logger.debug(f"post_info. User: {user_data}")
    data = complex_service(
        request.countryFrom,
        request.countryTo,
        request.isCapital == True,
        request.isWeather == True,
        request.isCurrency == True
    )
    return travel_response_mapper(data)

@travel_router.get("/", response_model=TravelResponse, response_model_exclude_none=True)
async def get_info(request: TravelRequest = Depends(), user_data = Depends(get_current_admin_user)) -> TravelResponse:
    logger.debug(f"get_info. Request: {request}")
    logger.debug(f"get_info. User: {user_data}")
    data = complex_service(request.countryFrom, request.countryTo, True, True, True)
    return travel_response_mapper(data)