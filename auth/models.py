from pydantic import BaseModel
from users import User

class LoginRequest(BaseModel):
    username: str
    password: str

class AuthUser(User):
    hashed_password: str