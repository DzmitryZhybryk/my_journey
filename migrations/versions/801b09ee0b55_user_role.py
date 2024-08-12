"""user_role

Revision ID: 801b09ee0b55
Revises: 82f2c0d925d6
Create Date: 2024-08-11 15:36:22.224315

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '801b09ee0b55'
down_revision: Union[str, None] = '82f2c0d925d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

role_enum = sa.Enum('base', 'moderator', 'admin', name='role_enum')


def upgrade() -> None:
    role_enum.create(op.get_bind())
    op.add_column('users', sa.Column('role', role_enum, nullable=True))
    op.execute("UPDATE users SET role = 'base'")
    op.alter_column('users', 'role', nullable=False)


def downgrade() -> None:
    op.drop_column('users', 'role')
    role_enum.drop(op.get_bind())
