"""backfill coupons

Revision ID: 1b6df6316c0e
Revises: d0bb82c7c088
Create Date: 2026-08-18 21:04:17.217811

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b6df6316c0e'
down_revision: Union[str, Sequence[str], None] = 'd0bb82c7c088'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "orders",
        sa.Column("coupon_id", sa.String())
    )

    op.execute("""
        UPDATE orders
        SET coupon_id='1'
    """)



def downgrade() -> None:
    op.drop_column("orders", "coupon_id")
