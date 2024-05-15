import typing
from typing import Any, Sequence

import sqlalchemy as sa
from sqlalchemy import ScalarResult, Row
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app import models
from app.config import settings
from app.handlers import welcome, travel

DATABASE_URL = (f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
                f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DATABASE}")

async_engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)


class DBWorker:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.travel_table = models.Travel
        self.user_table = models.User

    async def add_new_travel(self, new_travel_schema: travel.AddTravelSchema) -> None:
        async with self.session as session:
            stmt = sa.insert(self.travel_table).values(
                **new_travel_schema.model_dump()
            )
            await session.execute(stmt)
            await session.commit()

    async def get_all_travels(self, user_id: int) -> ScalarResult[models.Travel]:
        async with self.session as session:
            stmt = sa.select(
                self.travel_table
            ).where(
                self.travel_table.__table__.c.user_id == user_id,
                self.travel_table.__table__.c.deleted_date.is_(None),
            ).order_by(
                self.travel_table.travel_year
            )
            response = await session.execute(stmt)
            return response.scalars()

    async def get_distance(self, user_id: int, transport_type: str) -> float:
        async with self.session as session:
            stmt = sa.select(
                sa.func.sum(self.travel_table.distance)
            ).where(
                self.travel_table.__table__.c.transport_type == transport_type,
                self.travel_table.__table__.c.user_id == user_id,
                self.travel_table.__table__.c.deleted_date.is_(None),
            )
            result = await session.execute(stmt)
            distance = result.scalar()
            return distance or 0

    async def get_travel_count(self, user_id: int, transport_type: str) -> int:
        async with self.session as session:
            stmt = sa.select(
                sa.func.count(self.travel_table.travel_id)
            ).where(
                self.travel_table.__table__.c.transport_type == transport_type,
                self.travel_table.__table__.c.user_id == user_id,
                self.travel_table.__table__.c.deleted_date.is_(None),
            )
            result = await session.execute(stmt)
            count = result.scalar()
            return count or 0

    async def get_all_countries(self, user_id: int) -> Sequence[Row[tuple[Any, ...] | Any]]:
        async with self.session as session:
            from_subquery = sa.select(
                self.travel_table.location["from_"]["country"],
            ).where(
                self.travel_table.__table__.c.user_id == user_id,
                self.travel_table.__table__.c.deleted_date.is_(None),
            )

            to_subquery = sa.select(
                self.travel_table.location["to"]["country"],
            ).where(
                self.travel_table.__table__.c.user_id == user_id,
                self.travel_table.__table__.c.deleted_date.is_(None),
            )

            stmt = sa.union(from_subquery, to_subquery)
            result = await session.execute(stmt)
            return result.fetchall()

    async def delete_travel(self, user_id: int, travel_id: int) -> None:
        async with self.session as session:
            stmt = sa.update(
                self.travel_table
            ).where(
                self.travel_table.__table__.c.user_id == user_id,
                self.travel_table.__table__.c.travel_id == travel_id,
            ).values(
                deleted_date=sa.func.now()
            )
            await session.execute(stmt)
            await session.commit()

    async def get_travel_by_id(self, travel_id: int) -> models.Travel | None:
        async with self.session as session:
            stmt = sa.select(
                self.travel_table,
            ).where(
                self.travel_table.__table__.c.travel_id == travel_id
            )
            result = await session.execute(stmt)
            return result.scalar()

    async def add_user(self, user: welcome.AddUserSchema) -> None:
        async with self.session as session:
            stmt = sa.insert(
                self.user_table
            ).values(
                **user.model_dump()
            )
            await session.execute(stmt)
            await session.commit()

    async def get_user(self, user_id: int) -> models.User | None:
        async with self.session as session:
            stmt = sa.select(
                self.user_table
            ).where(
                self.user_table.__table__.c.telegram_id == user_id
            )
            result = await session.execute(stmt)
            return result.scalar()

    async def update_user(self, user_id: int, **kwargs: typing.Any) -> None:
        async with self.session as session:
            stmt = sa.update(
                self.user_table
            ).where(
                self.user_table.__table__.c.telegram_id == user_id
            ).values(
                **kwargs,
                updated_date=sa.func.now(),
            )
            await session.execute(stmt)
            await session.commit()


storage = DBWorker(session=async_session())
