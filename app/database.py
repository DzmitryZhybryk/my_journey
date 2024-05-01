import sqlalchemy as sa
from sqlalchemy import ScalarResult
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app import models
from app import schemas
from app.config import settings

DATABASE_URL = (f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
                f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DATABASE}")

async_engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)


class DBWorker:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_new_travel(self, new_travel_schema: schemas.AddTravelSchema) -> None:
        async with self.session as session:
            stmt = sa.insert(models.Travel).values(
                **new_travel_schema.model_dump()
            )
            await session.execute(stmt)
            await session.commit()

    async def get_all_travels(self, user_id: int) -> ScalarResult[models.Travel]:
        async with self.session as session:
            stmt = sa.select(
                models.Travel
            ).where(
                models.Travel.user_id == user_id
            ).order_by(
                models.Travel.travel_year
            )
            response = await session.execute(stmt)
            return response.scalars()

    async def add_user(self, user: schemas.AddUserSchema) -> None:
        async with self.session as session:
            stmt = sa.insert(
                models.User
            ).values(
                **user.model_dump()
            )
            await session.execute(stmt)
            await session.commit()

    async def get_user(self, user_id: int) -> models.User | None:
        async with self.session as session:
            stmt = sa.select(
                models.User
            ).where(
                models.User.telegram_id == user_id
            )
            result = await session.execute(stmt)
            return result.scalar()

    async def get_distance(self, user_id: int, transport_type: str) -> float:
        async with self.session as session:
            stmt = sa.select(
                sa.func.sum(models.Travel.distance)
            ).where(
                models.Travel.transport_type == transport_type,
                models.Travel.user_id == user_id,
            )
            result = await session.execute(stmt)
            distance = result.scalar()
            return distance or 0

    async def get_all_countries(self, user_id: int) -> ScalarResult[models.Travel]:
        async with self.session as session:
            from_subquery = sa.select(
                models.Travel.location["from_"]["country"],
            ).where(
                models.Travel.user_id == user_id
            )

            to_subquery = sa.select(
                models.Travel.location["to"]["country"],
            ).where(
                models.Travel.user_id == user_id
            )

            stmt = sa.union(from_subquery, to_subquery)
            result = await session.execute(stmt)
            return result.scalars()


storage = DBWorker(session=async_session())
