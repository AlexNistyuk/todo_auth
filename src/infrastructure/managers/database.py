from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from infrastructure.config import get_settings
from infrastructure.managers.interfaces import IManager

settings = get_settings()

print(settings.db_url)


class DatabaseManager(IManager):
    """Database manager. Create engine and async session maker"""

    engine: AsyncEngine = create_async_engine(
        settings.db_url,
        pool_size=settings.db_pool_size,
        max_overflow=settings.db_max_overflow,
    )
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

    @classmethod
    async def connect(cls):
        return cls

    @classmethod
    async def close(cls):
        await cls.engine.dispose()
