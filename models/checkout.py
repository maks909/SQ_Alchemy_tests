import sqlalchemy as sa

from models.base import Model
from schemas.shipment_state_schema import ShipmentStateSchema


class Checkout(Model):
    __tablename__ = "checkout"
    id = sa.Column(sa.Integer, primary_key=True)
    item_id = sa.Column(sa.Integer, sa.ForeignKey("item.id", ondelete="SET NULL"))
    price = sa.Column(sa.Numeric(10, 2), nullable=False)
    amount = sa.Column(sa.Integer)
    reciept_id = sa.Column(sa.Integer, sa.ForeignKey("receipt.id", ondelete="CASCADE"))


