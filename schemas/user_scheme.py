from typing import Optional

from pydantic import BaseModel


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
