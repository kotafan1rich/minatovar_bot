"""change_size_type

Revision ID: f0dbb67824ea
Revises: c9c2c47ccd99
Create Date: 2025-02-15 18:04:38.561803

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0dbb67824ea'
down_revision: Union[str, None] = 'c9c2c47ccd99'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('orders', 'size',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               type_=sa.String(length=100),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('orders', 'size',
               existing_type=sa.String(length=100),
               type_=sa.DOUBLE_PRECISION(precision=53),
               existing_nullable=False)
    # ### end Alembic commands ###
