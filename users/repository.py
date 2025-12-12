from typing import Optional
from users.models import User, ADMIN_ROLE, USER_ROLE


class UserRepository:
    def __init__(self) -> None:
        self.mock_data: dict[str, User] = {
            "user": User(username="user", role=USER_ROLE),
            "admin": User(username="admin", role=ADMIN_ROLE)
        }

    def get_by_username(self, username: str) -> Optional[User]:
        return self.mock_data.get(username)
    
    