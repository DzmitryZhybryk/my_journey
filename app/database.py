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

    def __init__(self, session: AsyncSession):
        self.session = async_session()

    async def add_new_trip(self, user_id: int) -> None:
        async for connect in self.session:
            stmt = sa.insert(models.Country).values(
                name="Belarus",
                user_id=123123123,
            )
            await connect.execute(stmt)
            await connect.commit()

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
