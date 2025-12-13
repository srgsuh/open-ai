from fastapi import APIRouter, HTTPException, status
from .models import AuthUser
from .repository import get_auth_user
from .hashing import verify
from .jwt import issue_token
from auth.models import LoginRequest, LoginResponse
from logs import logger

auth_router = APIRouter()

@auth_router.post("/login", response_model=LoginResponse)
async def post_login(request: LoginRequest) -> LoginResponse:
    logger.debug(f"post_login. request={request}")
    auth_user: AuthUser | None = get_auth_user(request.username)
    if auth_user and verify(request.password, auth_user.hashed_password):
        return LoginResponse(token=issue_token(auth_user), token_type="bearer")
    
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Wrong credentials")
    