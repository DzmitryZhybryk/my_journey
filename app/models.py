from datetime import datetime, timezone
from enum import StrEnum

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects import postgresql


class RoleEnum(StrEnum):
    base = "base"
    moderator = "moderator"
    admin = "admin"

    @classmethod
    def get_roles(cls):
        return {role.value for role in cls}


class Base(AsyncAttrs, DeclarativeBase):
    pass


class DateFieldMixin:
    created_date: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_date: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=True
    )
    deleted_date: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=True
    )


class User(Base, DateFieldMixin):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(sa.String(255))
    username: Mapped[str] = mapped_column(sa.String(255))
    birthday: Mapped[datetime] = mapped_column(sa.Date, nullable=True)
    nickname: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    role: Mapped[RoleEnum] = mapped_column(postgresql.ENUM(RoleEnum, name="role_enum"), default=RoleEnum.base)
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=True)


class Travel(Base, DateFieldMixin):
    __tablename__ = "travels"

    travel_id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    distance: Mapped[float] = mapped_column(sa.Float)
    transport_type: Mapped[str] = mapped_column(sa.String(255))
    travel_year: Mapped[int] = mapped_column(sa.Integer)
    user_id: Mapped[int] = mapped_column(sa.Integer)
    location: Mapped[dict[str, str]] = mapped_column(
        JSONB(astext_type=sa.Text(), none_as_null=True), nullable=False,
    )
