from typing import Optional

mock_user_data: dict[str, dict] = {
    "user": {
        "username": "user",
        "role": "USER",
        "hashed_password": "1"
    },
    "subscriber": {
        "username": "subscriber",
        "role": "USER",
        "hashed_password": "1"
    },
    "admin": {
        "username": "admin",
        "role": "ADMIN",
        "hashed_password": "1"
    }
}

def get_db_user(username: str) -> Optional[dict]:
    return mock_user_data.get(username)

__all__ = ["get_db_user"]