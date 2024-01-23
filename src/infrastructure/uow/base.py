from typing import Type

from infrastructure.managers.database import DatabaseManager
from infrastructure.repositories.interfaces import IRepository
from infrastructure.uow.interfaces import IUnitOfWork


class BaseUnitOfWork(DatabaseManager, IUnitOfWork):
    """Base unit of work"""

    repository: Type[IRepository]

    async def __aenter__(self):
        self.session = self.async_session_maker()
        self.repo = self.repository(self.session)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
