from fastapi import APIRouter
import sqlalchemy as sa

from app.database import SessionDep
from models import User
from schemas.user_scheme import CreateUserSchema

user_router = APIRouter()

@user_router.post("")
async def user_add(session: SessionDep, user_data: CreateUserSchema):
    q = sa.insert(User).values({
        User.name: user_data.name,
        User.password: user_data.password,
        User.email: user_data.email
    }
    )
    await session.execute(q)

@user_router.delete("/{user_id}")
async def user_delete(user_id: int):
    pass

@user_router.post("/{user_id}")
async def user_update(user_id: int):
    pass

@user_router.get("/{user_id}")
async def user_read(user_id: int):
    pass

