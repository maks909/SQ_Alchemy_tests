import sqlalchemy as sa

from models.base import Model
from schemas.shipment_state_schema import ShipmentStateSchema


class Receipt(Model):
    __tablename__ = "receipt"
    id = sa.Column(sa.Integer, primary_key=True)
    price = sa.Column(sa.Numeric(10, 2), nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("user.id", ondelete="SET NULL"))
    state: ShipmentStateSchema = sa.Column(
        sa.String, nullable=False, server_default=ShipmentStateSchema.CREATED
    )
    timestamp = sa.Column(
        sa.DateTime(timezone=False),
        nullable=False,
        server_default=sa.text("statement_timestamp()"),
    )