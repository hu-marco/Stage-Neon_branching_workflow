"""add product_review

Revision ID: 8cfa6e05f3b3
Revises: 9f9fe3b56a4f
Create Date: 2026-08-22 19:25:57.178960

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8cfa6e05f3b3'
down_revision: Union[str, Sequence[str], None] = 'f82eff2b844f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "products",
        sa.Column("product_review", sa.String())
    )


def downgrade() -> None:
    op.drop_column("products", "product_review")
