from typing import Optional

import jwt
from config import settings
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED
from JWT_utils import decode_token

from .tokens import JWTAuthToken


class OAuth2JWT(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[JWTAuthToken]:
        token = await super().__call__(request)

        if not token:
            return

        try:
            jwt_token = decode_token(token)
            # if not settings.DEBUG and jwt_token.identity == "debug":
            #     raise HTTPException(
            #         status_code=HTTP_401_UNAUTHORIZED,
            #         detail="Invalid token",
            #         headers={"WWW-Authenticate": "Bearer"},
            #     )
            return jwt_token
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Signature has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.PyJWTError as e:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Could not decode token",
                headers={"WWW-Authenticate": "Bearer"},
            )


oauth2_scheme = OAuth2JWT("/auth/login", auto_error=True)
