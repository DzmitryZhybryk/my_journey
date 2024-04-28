from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


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


class Country(Base, DateFieldMixin):
    __tablename__ = "countries"

    country_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(Integer)


class Travel(Base, DateFieldMixin):
    __tablename__ = "travels"

    travel_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_town: Mapped[str] = mapped_column(String(255))
    second_town: Mapped[str] = mapped_column(String(255))
    distance: Mapped[int] = mapped_column(Integer)
    transport_type: Mapped[str] = mapped_column(String(255))
    travel_year: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer)
