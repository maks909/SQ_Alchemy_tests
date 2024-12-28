from typing import Optional

import sqlalchemy as sa
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from db import get_session_dep
from models.user import UserModel
from schemas.security import TokenData
from schemas.user import UserSchema
from utils.hasher import Hasher
from utils.jwt_utils import decode_token

hasher = Hasher()


class Oauth2Scheme(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> TokenData:
        token = await super().__call__(request)
        payload = decode_token(token)
        return TokenData(**payload)

    def user(self) -> UserSchema:
        async def wrapper(
            token: TokenData = Depends(self),
            session: AsyncSession = get_session_dep,
        ):
            q = sa.select(UserModel.__table__.c).where(UserModel.id == token.sub)
            r = (await session.execute(q)).mappings().first()
            return UserSchema(**r)

        return Depends(wrapper)


async def get_user_by_id(session: AsyncSession, user_id: int) -> Optional[UserSchema]:
    q = sa.select(UserModel.__table__.c).where(UserModel.id == user_id)
    user = (await session.execute(q)).mappings().first()
    if user:
        return UserSchema(**user)


async def get_user_by_username(
    session: AsyncSession, username: str
) -> Optional[UserSchema]:
    q = sa.select(UserModel.__table__.c).where(UserModel.username == username)
    user = (await session.execute(q)).mappings().first()
    if user:
        return UserSchema(**user)


async def authenticate_user(
    session: AsyncSession, username: str, password: str
) -> UserSchema:
    q = sa.select(
        UserModel.id,
        UserModel.password,
    ).where(UserModel.username == username)
    data = (await session.execute(q)).fetchone()

    if not data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username",
        )
    if not hasher.verify_password(password, data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
        )
    user = await get_user_by_id(session, data.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


oauth2_scheme = Oauth2Scheme(tokenUrl="v1/login")
