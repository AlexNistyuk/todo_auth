from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from infrastructure.config import get_settings
from infrastructure.managers.interfaces import IManager

settings = get_settings()


class DatabaseManager(IManager):
    engine: AsyncEngine = create_async_engine(settings.db_url)
    # async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False

    @classmethod
    async def connect(cls):
        return cls

    @classmethod
    async def close(cls):
        await cls.engine.dispose()
