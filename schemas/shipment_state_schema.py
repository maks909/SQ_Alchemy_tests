from enum import Enum


class ShipmentStateSchema(str, Enum):
    CREATED = "CREATED"
    PAID = "PAID"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
