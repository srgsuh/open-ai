from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
import requests
from configuration import get_config_parameter

user_pool_id = get_config_parameter("USER_POOL_ID")
region_id = get_config_parameter("AWS_REGION_ID")
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
        raise invalid_token
    return key_id

def get_current_token(token: str = Depends(oauth2_scheme)) -> dict:
    kid = extract_kid(token)
    keys = fetch_cognito_keys()

    public_key: dict | None = next((k for k in keys if k["kid"] == kid), None)

    if not public_key:
        raise invalid_token
    
    payload: dict
    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=public_key["alg"],
            issuer=COGNITO_ISSUER,
            options={"verify_aud": False}
        )
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="The access token provided is expired", headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
        raise invalid_token
    
    return payload

def get_current_access_token(payload: dict = Depends(get_current_token)) -> dict:
    if payload.get("token_use") != "access":
        raise invalid_token

    return payload