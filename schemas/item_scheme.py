from typing import Optional

from pydantic import BaseModel


class CreateItemSchema(BaseModel):
    name: str
    description: str
    price: float


class ItemSchema(BaseModel):
    id: int
    name: str
    description: str
    price: float


class UpdateItemSchema(BaseModel):
    name: str | None
    description: str | None
    price: float | None
