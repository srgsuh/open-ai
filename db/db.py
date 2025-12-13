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

def get_db_user(username: str) -> Optional[dict]:
    return mock_user_data.get(username)

__all__ = ["get_db_user"]