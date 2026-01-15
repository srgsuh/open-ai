from fastapi import Depends
from auth.cognito_token import get_current_access_token, get_current_admin_token

def get_current_user(payload: dict = Depends(get_current_access_token)) -> dict:
    return payload

def get_current_admin_user(payload: dict = Depends(get_current_admin_token)) -> dict:
    return payload