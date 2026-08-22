"""add phone number

Revision ID: 9f9fe3b56a4f
Revises: d7b873c2a0a0
Create Date: 2026-08-22 19:25:40.194366

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f9fe3b56a4f'
down_revision: Union[str, Sequence[str], None] = 'f82eff2b844f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("phone_number", sa.String())
    )


def downgrade() -> None:
    op.drop_column("users", "phone_number")
