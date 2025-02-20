from pydantic import BaseModel
from datetime import datetime
from shipment_state_schema import ShipmentStateSchema


class CheckoutSchema(BaseModel):
    id: int
    item_id: int
    timestamp: datetime
    amount: int
    price: float
    state: ShipmentStateSchema
