from fastapi import APIRouter, HTTPException
from .models import AuthUser
from .repository import get_auth_user
from .hashing import verify
from auth.models import LoginRequest, LoginResponse

auth_router = APIRouter()

@auth_router.post("/login", response_model=LoginResponse)
def post_login(request: LoginRequest) -> LoginResponse:
    auth_user: AuthUser | None = get_auth_user(request.username)
    if auth_user and verify(request.password, auth_user.hashed_password):
        return LoginResponse(token="token", token_type="bearer")
    raise HTTPException(401, detail="Wrong credentials")
    