from datetime import datetime, timedelta

import jwt

from config import settings

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.API_SECRET_KEY, algorithms=["HS256"])


def create_jwt_access_token(user_id: int) -> str:
    now = datetime.utcnow()
    data_to_encode = {
        "sub": user_id,
        "iat": now,
        "exp": now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    encoded_refresh_jwt = jwt.encode(
        data_to_encode,
        settings.API_SECRET_KEY,
    )
    return encoded_refresh_jwt


def create_jwt_refresh_token(user_id: int) -> str:
    now = datetime.utcnow()
    data_to_encode = {
        "sub": user_id,
        "iat": now,
        "exp": now + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
    }
    encoded_access_jwt = jwt.encode(
        data_to_encode,
        settings.API_SECRET_KEY,
    )
    return encoded_access_jwt
