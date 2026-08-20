"""add total price to orders

Revision ID: f82eff2b844f
Revises: 2f133e768707
Create Date: 2026-08-19 22:06:16.485721

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f82eff2b844f'
down_revision: Union[str, Sequence[str], None] = '2f133e768707'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "orders",
        sa.Column("total_price", sa.Numeric(10, 2), nullable=True)
    )
    
    op.execute("""
        UPDATE orders
        SET total_price = COALESCE((
        SELECT SUM(price * quantity)
        from products p INNER JOIN  order_items o 
        ON p.id = o.product_id
        WHERE orders.id= o.order_id
        ),0);
    """)
    



def downgrade() -> None:
    op.drop_column("orders", "total_price")
