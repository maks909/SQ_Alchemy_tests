from models.base import Model
import sqlalchemy as sa

class Item(Model):
    __tablename__ = "item"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    price = sa.Column(sa.Integer)
    description = sa.Column(sa.String)
    
