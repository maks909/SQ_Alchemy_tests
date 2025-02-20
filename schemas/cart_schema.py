from pydantic import BaseModel


class CartSchema(BaseModel):
    item_id: int
    amount: int
