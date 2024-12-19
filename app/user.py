import sqlalchemy as sa
from fastapi import APIRouter, HTTPException, Body
from starlette import status

from app.database import SessionDep
from models import User
from schemas.user_scheme import CreateUserSchema, UserSchema, UpdateUserSchema

user_router = APIRouter()


@user_router.post("", response_model=int)
async def user_add(session: SessionDep, user_data: CreateUserSchema):
    q = (
        sa.insert(User)
        .values(
            {
                User.name: user_data.name,
                User.password: user_data.password,
                User.email: user_data.email,
            }
        )
        .returning(User.id)
    )
    # user_id = (await session.execute(q)).mappings().fetchall()
    # user_id = (await session.execute(q)).mappings().fetchone()
    user_id = (await session.execute(q)).scalar()
    return user_id


@user_router.delete("/{user_id}", response_model=int)
async def user_delete(user_id: int, session: SessionDep):
    q = sa.delete(User).where(User.id == user_id).returning(User.id)
    user_id = (await session.execute(q)).scalar()
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user_id


@user_router.post("/{user_id}")
async def user_update(user_id: int, session: SessionDep, user_data: UpdateUserSchema=Body(...)):
    q = (
        sa.update(User)
        .where(User.id == user_id)
        .values(**user_data.model_dump(exclude_unset=True))
        .returning(User.id, User.name, User.email)
    )

    response = (await session.execute(q)).mappings().fetchone()

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return response


@user_router.get("/{user_id}", response_model=UserSchema)
async def user_read(user_id: int, session: SessionDep):
    q = sa.select(User.name, User.email, User.id).where(User.id == user_id)

    response = (await session.execute(q)).mappings().fetchone()
    return response
