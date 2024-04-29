import sqlalchemy as sa

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app import models

from app.config import settings
from app import schemas

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
            user = result.scalar()
            return user


storage = DBWorker(session=async_session())
