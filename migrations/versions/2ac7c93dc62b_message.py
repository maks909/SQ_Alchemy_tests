"""message

Revision ID: 2ac7c93dc62b
Revises: efe03556ca6d
Create Date: 2024-12-12 19:12:51.514534

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ac7c93dc62b'
down_revision: Union[str, None] = 'efe03556ca6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email', sa.String(), nullable=False))
    op.add_column('user', sa.Column('password', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'password')
    op.drop_column('user', 'email')
    # ### end Alembic commands ###
