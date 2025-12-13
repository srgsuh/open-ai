from pydantic import BaseModel
from users import User

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    token: str
    token_type: str

class AuthUser(User):
    hashed_password: str