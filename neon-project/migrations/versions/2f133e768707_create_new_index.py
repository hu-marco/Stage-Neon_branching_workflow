"""create new index

Revision ID: 2f133e768707
Revises: 1b6df6316c0e
Create Date: 2026-08-19 11:22:51.205363

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f133e768707'
down_revision: Union[str, Sequence[str], None] = '1b6df6316c0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index('idx_orders_created', 'orders', ['created_at'], unique=True)

def downgrade() -> None:
    op.drop_index('idx_orders_created', table_name='orders')
