import traceback
from auth.models import AuthUser
from fastapi import status, Depends, HTTPException
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from models.user import User
from users import get_by_username
from configuration import get_config_parameter
from datetime import datetime, timedelta, timezone
import jwt
from logs import logger

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

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    parts = token.split(".")
    logger.debug(f"jwt(4)={token[:5]}, parts={len(parts)}, lengths={[len(p) for p in parts]}")
    username : str | None = None
    user: User | None = None
    try:
        payload: dict = jwt.decode(
            jwt = token,
            key = _get_secret_key(),
            algorithms=["HS256"]
        )
        logger.debug(f"get_current_user. payload={payload}")
        username = payload.get("sub")
    except Exception as e:
        logger.error(f"JWT decode failed. error={e}, type={type(e)}\n{traceback.format_exc()}")
    
    user = get_by_username(username) if username else None
    logger.debug(f"get_current_user. user={user}")
    if user:
        return user
    
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Illegal token")

async def require_admin(user: Annotated[User, Depends(get_current_user)]) -> User:
    if not user.is_admin():
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Unauthorized access")
    return user