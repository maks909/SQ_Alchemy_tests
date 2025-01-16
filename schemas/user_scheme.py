from typing import Optional

from pydantic import BaseModel, Field


class CreateUserSchema(BaseModel):
    name: str
    password: str
    email: str


class UserSchema(BaseModel):
    id: int
    name: str
    email: str

class UpdateUserSchema(BaseModel):
    name: str | None
    password: str | None
    email: str | None

class AuthUserSchema(BaseModel):
    grant_type: str
    password: str
    name: str = Field(..., alias="username")
