from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from logs import logger
from auth import require_admin
from users.models import User
from users import get_statistics

class UserStatistics(BaseModel):
    username: str
    requests: int

users_router = APIRouter()
@users_router.get("/statistics", response_model=dict[str, int])
async def get_users_statistics(role: Optional[str] = None, user: User = Depends(require_admin)) -> dict[str, int]:
    logger.debug(f"get_users_statistics. role={role}, user={user}")
    return get_statistics(role)