"""add CAP column

Revision ID: d555aff7f21e
Revises: 
Create Date: 2026-08-30 22:27:47.635269

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd555aff7f21e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "addresses",
        sa.Column("CAP", sa.String())
    )


def downgrade() -> None:
    op.drop_column("addresses", "CAP")
