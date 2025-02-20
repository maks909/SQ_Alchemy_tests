import sqlalchemy as sa
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas.user_scheme import UserSchema
from .hasher import Hasher
from utils.user_utils import get_user_by_id

hasher = Hasher()


async def authenticate_user(
    session: AsyncSession, username: str, password: str
) -> UserSchema:
    q = sa.select(
        User.id,
        User.password,
    ).where(User.name == username)
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
