"""create coupons table

Revision ID: d0bb82c7c088
Revises: 
Create Date: 2026-08-09 22:32:22.119844

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0bb82c7c088'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "coupons",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String()),
        sa.Column("discount", sa.Integer())
    )



def downgrade() -> None:
    op.drop_table("coupons")
