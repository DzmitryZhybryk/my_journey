"""user_active

Revision ID: 58a3e5029fa2
Revises: 801b09ee0b55
Create Date: 2024-08-13 11:29:56.004875

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '58a3e5029fa2'
down_revision: Union[str, None] = '801b09ee0b55'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.execute("UPDATE users SET is_active = TRUE")
    op.alter_column('users', 'is_active', nullable=False)


def downgrade() -> None:
    op.drop_column('users', 'is_active')
