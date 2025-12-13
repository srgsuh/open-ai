from typing import Optional
from users.models import User, ADMIN_ROLE, USER_ROLE
from db import get_db_user

def get_by_username(username: str) -> Optional[User]:
    user: Optional[User] = None
    user_data: Optional[dict] = get_db_user(username)
    if user_data:
        user = User(username=user_data["username"], role=user_data["role"])
    
    return user