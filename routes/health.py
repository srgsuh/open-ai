from fastapi import APIRouter

health_router: APIRouter = APIRouter()

@health_router.get("/health")
async def get_health() -> dict:
    return {"status" : "OK"}