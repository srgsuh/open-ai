from fastapi import APIRouter
from logs import logger
from models.TravelRequest import TravelRequest
from models.TravelResponse import TravelResponse

travel_router = APIRouter()

@travel_router.post("/info", response_model=TravelResponse, response_model_exclude_none=True)
async def post_info(request: TravelRequest) -> TravelResponse:
    logger.debug(f"post_info. Request: {request}")

    return TravelResponse(
        countryFrom=request.countryFrom,
        countryTo=request.countryTo,
        capitalTo="London",
        weatherTo="chilly"
    )