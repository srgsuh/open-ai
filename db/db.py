from typing import Optional

mock_user_data: dict[str, dict] = {
    "user": {
        "username": "user",
        "role": "USER",
        "hashed_password": "$2a$10$.MUNrJCapAU8oOAnP6muLewjywqkzJE7PD4VFipmFJyZvY9AU6Rza"
    },
    "subscriber": {
        "username": "subscriber",
        "role": "USER",
        "hashed_password": "$2a$10$un6BRatml4BSZPA0PlI8oebYswVLWe9wq48C6h0v/xRd2W6TY96z2"
    },
    "admin": {
        "username": "admin",
        "role": "ADMIN",
        "hashed_password": "$2a$10$JMolw8a3b/trMkdQfxg8jOvlLMY9tNU7FHFeGDgHOuINbR/RG5y4i"
    }
}

statistics: dict[str, int] = {}

def get_db_user(username: str) -> Optional[dict]:
    return mock_user_data.get(username)

def get_all_db_users() -> list[dict]:
    return [v for v in mock_user_data.values()]

def get_statistics(role: Optional[str]) -> dict[str, int]:
    return {
        k: statistics.get(k, 0) for k in mock_user_data if (not role or mock_user_data[k]["role"] == role)
    }

def increase_statistics(username: str) -> None:
    statistics[username] = 1 + statistics.get(username, 0)

__all__ = ["get_db_user", "get_all_db_users", "get_statistics", "increase_statistics"]