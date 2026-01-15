from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
import requests
from configuration import get_config_parameter
from logs import get_logger

logger = get_logger("auth")

region_id = get_config_parameter("AWS_REGION_ID")
user_pool_id = get_config_parameter("USER_POOL_ID")
app_id = get_config_parameter("USER_POOL_APP_ID")

COGNITO_ISSUER = (
    f"https://cognito-idp.{region_id}.amazonaws.com/{user_pool_id}"
)
COGNITO_JWKS_URL = f"{COGNITO_ISSUER}/.well-known/jwks.json"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

invalid_token = HTTPException(status_code=401, detail="Wrong token", headers={"WWW-Authenticate": "Bearer"})

def fetch_cognito_keys() -> list[dict]:
    response: requests.Response = requests.get(COGNITO_JWKS_URL)
    response.raise_for_status()
    jwks: dict = response.json()
    return jwks.get("keys", [])

def extract_kid(token: str) -> str:
    header: dict = jwt.get_unverified_header(token)
    key_id = header.get("kid")
    if not key_id:
        logger.debug("No key ID found")
        raise invalid_token
    return key_id

def get_current_access_token(token: str = Depends(oauth2_scheme)) -> dict:
    logger.debug(".get_current_token token=%s...%s", token[:5], token[-5:])
    kid = extract_kid(token)
    keys = fetch_cognito_keys()

    public_key: Optional[dict] = next((k for k in keys if k["kid"] == kid), None)

    if not public_key:
        logger.debug("Public key is not found")
        raise invalid_token
    
    payload: dict
    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=public_key.get("alg", "RS256"),
            issuer=COGNITO_ISSUER
        )
    except ExpiredSignatureError:
        logger.debug("Expired token")
        raise invalid_token
    except JWTError as je:
        logger.error(f"JWTError occurred: \"%s\"", str(je))
        raise invalid_token
    
    token_type: Optional[str] = payload.get("token_use")
    if token_type != "access":
        logger.debug(f"Wrong type of token: {token_type}")
        raise invalid_token
    
    client_id: Optional[str] = payload.get("client_id")
    if client_id and client_id != app_id:
        logger.debug(f"Wrong app_id")
        raise invalid_token
    
    return payload


def is_admin_grp(grp_name: str) -> bool:
    return grp_name == "grp_administrators"

def get_current_admin_token(payload: dict = Depends(get_current_access_token)) -> dict:
    user_groups: list[str] = payload.get("cognito:groups", [])
    is_admin: bool = any((is_admin_grp(grp) for grp in user_groups))
    if not is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    return payload
        