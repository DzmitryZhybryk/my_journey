"""add_nickname_to_user

Revision ID: 82f2c0d925d6
Revises: ee8de75d2fec
Create Date: 2024-05-05 08:10:55.569724

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '82f2c0d925d6'
down_revision: Union[str, None] = 'ee8de75d2fec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('travels', 'location',
                    existing_type=postgresql.JSONB(astext_type=sa.Text()),
                    nullable=False)
    op.add_column('users', sa.Column('nickname', sa.String(length=255), nullable=True))
    op.alter_column('users', 'birthday', existing_type=sa.DateTime(), type_=sa.Date())


def downgrade() -> None:
    op.drop_column('users', 'nickname')
    op.alter_column('travels', 'location',
                    existing_type=postgresql.JSONB(astext_type=sa.Text()),
                    nullable=True)
    op.alter_column('users', 'birthday', existing_type=sa.Date(), type_=sa.DateTime())

