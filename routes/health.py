from fastapi import APIRouter

health_router: APIRouter = APIRouter()

@health_router.get("/")
async def get_health() -> dict:
    return {"status" : "OK"}