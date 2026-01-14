from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
import requests
from configuration import get_config_parameter


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
invalid_token = HTTPException(status_code=401, detail="Wrong token", headers={"WWW-Authenticate": "Bearer"})

def get_issuer() -> str:
    user_pool_id = get_config_parameter("USER_POOL_ID")
    region_id = get_config_parameter("AWS_REGION_ID")
    return f"https://cognito-idp.{region_id}.amazonaws.com/{user_pool_id}"

def cognito_jwks_url() -> str:
    issuer = get_issuer()
    return f"{issuer}/.well-known/jwks.json"

def get_cognito_keys() -> list[dict]:
    jwks_url: str = cognito_jwks_url()
    resp = requests.get(jwks_url)
    resp.raise_for_status()
    jwks: dict = resp.json()
    return jwks.get("keys", [])

def get_kid(token: str) -> str:
    header: dict = jwt.get_unverified_header(token)
    key_id = header.get("kid")
    if not key_id:
        raise invalid_token
    return key_id

def get_payload(token: str = Depends(oauth2_scheme)) -> dict:
    kid = get_kid(token)
    keys = get_cognito_keys()

    public_key: dict | None = next((k for k in keys if k["kid"] == kid), None)

    if not public_key:
        raise invalid_token
    
    payload: dict
    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=public_key["alg"],
            issuer=get_issuer(),
            options={
                "verify_signature": True,
                "verify_iss": True,
                "verify_exp": True,
                "verify_nbf": True,
                "verify_aud": False,  # Cognito access tokens don't use aud
                "leeway": 0,
            },
        )
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="The access token provided is expired", headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
        raise invalid_token
    
    return payload