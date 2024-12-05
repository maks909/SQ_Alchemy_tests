from models.base import Model
import sqlalchemy as sa

class User(Model):
    __tablename__ = "user"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
