from typing import Optional
from users.models import User, ADMIN_ROLE, USER_ROLE
import db

def get_by_username(username: str) -> Optional[User]:
    user: Optional[User] = None
    user_data: Optional[dict] = db.get_db_user(username)
    if user_data:
        user = User(username=user_data["username"], role=user_data["role"])
    
    return user

def increase_statistics(username: str) -> None:
    db.increase_statistics(username)

def get_statistics(role: Optional[str]) -> dict:
    return db.get_statistics(role)