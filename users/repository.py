from typing import Optional
from users.models import User, ADMIN_ROLE, USER_ROLE
from db import get_db_user


class UserRepository:
    def get_by_username(self, username: str) -> Optional[User]:
        user: Optional[User] = None
        user_data: Optional[dict] = get_db_user(username)
        if user_data:
            user = User(username=user_data["username"], role=user_data["role"])
        
        return user

user_repo: UserRepository = UserRepository()

def get_user_repo() -> UserRepository:
    return user_repo