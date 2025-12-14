from pydantic import BaseModel
from models.user import User

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    token: str
    token_type: str

class AuthUser(User):
    hashed_password: str