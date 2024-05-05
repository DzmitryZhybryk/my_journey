from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text, Float
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.dialects.postgresql import JSONB


class Base(AsyncAttrs, DeclarativeBase):
    pass


class DateFieldMixin:
    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    deleted_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class User(Base, DateFieldMixin):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))
    username: Mapped[str] = mapped_column(String(255))
    birthday: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    nickname: Mapped[str] = mapped_column(String(255), nullable=True)


class Travel(Base, DateFieldMixin):
    __tablename__ = "travels"

    travel_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    distance: Mapped[float] = mapped_column(Float)
    transport_type: Mapped[str] = mapped_column(String(255))
    travel_year: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer)
    location: Mapped[dict[str, str]] = mapped_column(
        JSONB(astext_type=Text(), none_as_null=True), nullable=False,
    )
