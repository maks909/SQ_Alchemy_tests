from typing import Optional

from pydantic import BaseModel


class CreateitemSchema(BaseModel):
    name: str
    description: str
    price: int

class itemSchema(BaseModel):
    id: int
    name: str
    description: str
    price: int

class UpdateitemSchema(BaseModel):
    name: str | None
    description: str | None
    price: int | None