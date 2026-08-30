"""delete addresses

Revision ID: b1540c141bb7
Revises: 
Create Date: 2026-08-30 22:01:02.370564

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1540c141bb7'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("addresses")


def downgrade() -> None:
    op.create_table(
        "coupons",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer()),
        sa.Column("city", sa.String()),
        sa.Column("street", sa.String())
    )
