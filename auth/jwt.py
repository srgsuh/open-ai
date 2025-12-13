from auth.models import AuthUser
from fastapi import status, Depends, HTTPException
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
import users
from configuration import get_config_parameter
from datetime import datetime, timedelta, timezone
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

DEFAULT_TOKEN_EXPIRE_MIN: str = "0"

def _get_secret_key() -> str:
    return get_config_parameter("SECRET_KEY")

def _get_token_expire_minutes() -> int:
    return int(get_config_parameter("TOKEN_EXPIRE_MIN", DEFAULT_TOKEN_EXPIRE_MIN))

def _now() -> datetime:
    return datetime.now(tz=timezone.utc)

def _payload(user: AuthUser, min_to_expire: int = 0) -> dict:
    now: datetime = _now()
    payload: dict = {
        "sub": user.username,
        "iat": now
    }
    if min_to_expire:
        payload["exp"] = now + timedelta(minutes=min_to_expire)
    
    return payload

def issue_token(user: AuthUser) -> str:
    return jwt.encode(
        payload=_payload(user, _get_token_expire_minutes()),
        key=_get_secret_key(),
        algorithm="HS256"
    )

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    username : str | None = None
    user: users.User | None = None
    try:
        payload: dict = jwt.decode(
            jwt = token,
            key = _get_secret_key(),
            algorithms=["HS256"]
        )
        username = payload.get("sub")
    except Exception as e:
        pass
    
    user = users.get_user_repo().get_by_username(username) if username else None
    if user:
        return user
    
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Illegal token")