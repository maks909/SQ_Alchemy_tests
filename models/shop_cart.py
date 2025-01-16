from models.base import Model
import sqlalchemy as sa


class Cart(Model):
    __tablename__ = "cart"
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("user.id", ondelete="CASCADE"))
    item_id = sa.Column(sa.Integer, sa.ForeignKey("item.id", ondelete="CASCADE"))
    amount = sa.Column(sa.Integer)
    __table_args__ = (sa.UniqueConstraint(user_id, item_id),)

