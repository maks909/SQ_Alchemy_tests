from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from models import User
from schemas.user_scheme import UserSchema


async def get_user_by_id(session: AsyncSession, user_id: int)-> UserSchema:
    q = sa.select(User.name, User.email, User.id).where(User.id == user_id)

    response = (await session.execute(q)).mappings().fetchone()

    return UserSchema(**response)