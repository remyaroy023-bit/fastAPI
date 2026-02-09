"""Create phone number for user column

Revision ID: e5f2c23b8d58
Revises: 
Create Date: 2026-01-28 13:05:28.832878

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5f2c23b8d58'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users',sa.Column('phone_number',sa.String(50), nullable = True))
    pass


def downgrade() -> None:
    op.drop_column('users','phone_number')
    pass
