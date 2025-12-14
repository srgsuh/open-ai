from fastapi import Depends
from auth import get_current_user
from models.user import User
from users.repository import increase_statistics

async def collect_user_statistics(user: User = Depends(get_current_user)) -> None:
    increase_statistics(user.username)