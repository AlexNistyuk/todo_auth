from infrastructure.managers.database import DatabaseManager
from infrastructure.repositories.interfaces import IRepository
from infrastructure.uow.interfaces import IUnitOfWork


class UnitOfWork(DatabaseManager, IUnitOfWork):
    def __init__(self, repository: IRepository):
        self.repository = repository

    async def __aenter__(self):
        self.session = self.async_session_maker()
        self.repository = self.repository(self.session)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
