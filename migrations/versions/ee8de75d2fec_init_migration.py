"""init_migration

Revision ID: ee8de75d2fec
Revises: 
Create Date: 2024-04-02 18:47:37.135273

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'ee8de75d2fec'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('travels',
                    sa.Column('travel_id', sa.Integer(), nullable=False),
                    sa.Column('location', sa.dialects.postgresql.JSONB(
                        astext_type=sa.Text(),
                        none_as_null=True
                    )),
                    sa.Column('distance', sa.Float(), nullable=False),
                    sa.Column('transport_type', sa.String(length=255), nullable=False),
                    sa.Column('travel_year', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('created_date', sa.DateTime(timezone=True), nullable=False),
                    sa.Column('updated_date', sa.DateTime(timezone=True), nullable=True),
                    sa.Column('deleted_date', sa.DateTime(timezone=True), nullable=True),
                    sa.PrimaryKeyConstraint('travel_id')
                    )

    op.create_table('users',
                    sa.Column('telegram_id', sa.Integer(), nullable=False),
                    sa.Column('full_name', sa.String(length=255), nullable=False),
                    sa.Column('username', sa.String(length=255), nullable=False),
                    sa.Column('birthday', sa.DateTime(timezone=True), nullable=True),
                    sa.Column('created_date', sa.DateTime(timezone=True), nullable=False),
                    sa.Column('updated_date', sa.DateTime(timezone=True), nullable=True),
                    sa.Column('deleted_date', sa.DateTime(timezone=True), nullable=True),
                    sa.PrimaryKeyConstraint('telegram_id')
                    )


def downgrade() -> None:
    op.drop_table('users')
    op.drop_table('travels')
