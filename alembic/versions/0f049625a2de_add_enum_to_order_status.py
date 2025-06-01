"""Add enum to order status

Revision ID: 0f049625a2de
Revises: 72c112d04a75
Create Date: 2025-06-01 15:28:29.978567

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Define the Enum
order_status_enum = postgresql.ENUM(
    'pending', 'processing', 'shipped', 'delivered', 'cancelled',
    name='orderstatus'
)

# revision identifiers, used by Alembic.
revision: str = '0f049625a2de'
down_revision: Union[str, None] = '72c112d04a75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create the enum type
    order_status_enum.create(op.get_bind())

    # Alter the column using explicit cast
    op.execute("""
        ALTER TABLE orders
        ALTER COLUMN status TYPE orderstatus
        USING status::orderstatus
    """)


def downgrade() -> None:
    """Downgrade schema."""
    # Revert column to VARCHAR using cast
    op.execute("""
        ALTER TABLE orders
        ALTER COLUMN status TYPE VARCHAR
        USING status::text
    """)

    # Drop the enum type
    order_status_enum.drop(op.get_bind())
