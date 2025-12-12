from typing import Optional
from users.models import User


class UserRepository:
    def __init__(self):
        self.mock_data: dict[str, User] = {
            "user": User("user", "user"),
            "admin": User("admin", "admin")
        }

    def get_by_username(self, username: str) -> Optional[User]:
        return self.mock_data.get(username)
    