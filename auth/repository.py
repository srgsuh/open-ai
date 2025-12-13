from typing import Optional
from auth.models import AuthUser
from db import get_db_user

def get_auth_user(username) -> Optional[AuthUser]:
    user_data = get_db_user(username)
    if user_data:
        return AuthUser(username=username, role=user_data["role"], hashed_password=user_data["hashed_password"])
    
    return None