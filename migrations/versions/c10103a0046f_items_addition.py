"""Items addition

Revision ID: c10103a0046f
Revises: 8f9ed42072c1
Create Date: 2025-02-20 18:37:10.846608

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c10103a0046f'
down_revision: Union[str, None] = '8f9ed42072c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('receipt',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_receipt'))
    )
    op.create_table('checkout',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('reciept_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.Column('state', sa.String(), server_default='CREATED', nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], name=op.f('fk_checkout_item_id_item'), ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['reciept_id'], ['receipt.id'], name=op.f('fk_checkout_reciept_id_receipt'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_checkout_user_id_user'), ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_checkout'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('checkout')
    op.drop_table('receipt')
    # ### end Alembic commands ###
