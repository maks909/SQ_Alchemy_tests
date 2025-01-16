from datetime import datetime, UTC, timedelta

import sqlalchemy as sa
from fastapi import APIRouter, HTTPException, Body, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.config import settings
from app.database import SessionDep
from models import User
from schemas.security_schema import OAuth2Response
from schemas.user_scheme import CreateUserSchema, UserSchema, UpdateUserSchema, AuthUserSchema
from utils.Oauth2_schema import oauth2_scheme
from utils.security import authenticate_user, hasher

from utils.JWT_utils import create_jwt_access_token


user_router = APIRouter()

@user_router.post("/login", response_model=OAuth2Response)
async def user_login(session: SessionDep, user_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(session, user_data.username, user_data.password)
    return OAuth2Response(
        access_token=create_jwt_access_token(user.id),
        expires_in=datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        user_name=user.name,
        user_id=user.id

    )



@user_router.post("", response_model=int)
async def user_add(session: SessionDep, user_data: CreateUserSchema):
    q = (
        sa.insert(User)
        .values(
            {
                User.name: user_data.name,
                User.password: hasher.get_password_hash(user_data.password),
                User.email: user_data.email,
            }
        )
        .returning(User.id)
    )
    # user_id = (await session.execute(q)).mappings().fetchall()
    # user_id = (await session.execute(q)).mappings().fetchone()
    user_id = (await session.execute(q)).scalar()
    return user_id


@user_router.get("/me", response_model=UserSchema)
async def user_me(session: SessionDep, token: dict=Depends(oauth2_scheme)):
    user_id = int(token["sub"])
    q=sa.select(User.name, User.email, User.id).where(User.id == user_id)
    user = (await session.execute(q)).mappings().fetchone()
    return user

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
