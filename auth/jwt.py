from auth.models import AuthUser
from configuration import get_config_parameter
from datetime import datetime, timedelta, timezone
import jwt

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
        "iat": now,
        "username": user.username,
        "role": user.role
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