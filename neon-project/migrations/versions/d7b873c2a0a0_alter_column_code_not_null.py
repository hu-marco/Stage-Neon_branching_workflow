"""alter column code not null

Revision ID: d7b873c2a0a0
Revises: f82eff2b844f
Create Date: 2026-08-19 22:27:03.044521

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7b873c2a0a0'
down_revision: Union[str, Sequence[str], None] = 'f82eff2b844f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    op.alter_column(
        "orders",
        "coupon_id",
        existing_type=sa.Integer(),
        nullable=False,
    )
    raise RuntimeError("Test migration failure")


def downgrade() -> None:
    op.alter_column(
        "coupons",
        "coupon_id",
        existing_type=sa.Integer(),
        nullable=True,
    )
