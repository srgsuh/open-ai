from passlib.hash import bcrypt
from configuration import get_config_parameter

DEFAULT_ROUNDS: str = "10"
bcrypt_rounds: int = int(get_config_parameter("BCRYPT_ROUNDS", DEFAULT_ROUNDS))

def hashing(payload: str) -> str:
    return bcrypt.using(rounds=bcrypt_rounds).hash(payload)

def verify(raw_payload: str, hashed_payload: str) -> bool:
    return bcrypt.verify(raw_payload, hashed_payload)