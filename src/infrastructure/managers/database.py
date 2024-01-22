from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from infrastructure.config import get_settings
from infrastructure.managers.interfaces import IManager

settings = get_settings()


class DatabaseManager(IManager):
    """Database manager. Create engine and async session maker"""

    engine: AsyncEngine = create_async_engine(settings.db_url)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

    @classmethod
    async def connect(cls):
        return cls

    @classmethod
    async def close(cls):
        await cls.engine.dispose()
