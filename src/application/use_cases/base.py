from typing import Sequence

from sqlalchemy import Row

from application.use_cases.interfaces import IUseCase
from infrastructure.repositories.interfaces import IRepository
from infrastructure.uow.base import UnitOfWork


class BaseUseCase(IUseCase):
    """Base use case"""

    repository: IRepository = None
    uow = UnitOfWork(repository)

    async def insert(self, data: dict) -> int:
        async with self.uow:
            result = await self.uow.repository.insert(data)

            await self.uow.commit()
        return result

    async def update_by_filters(self, data: dict, **filters) -> None:
        async with self.uow:
            await self.uow.repository.update_by_filters(data, **filters)
            await self.uow.commit()

    async def update_by_id(self, data: dict, record_id: int) -> int:
        async with self.uow:
            result = await self.uow.repository.update_by_id(data, record_id)

            await self.uow.commit()
        return result

    async def get_by_filters(self, **filters) -> Sequence:
        async with self.uow:
            return await self.uow.repository.get_by_filters(**filters)

    async def get_all(self) -> Sequence:
        async with self.uow:
            result = await self.uow.repository.get_all()

        return result

    async def get_by_id(self, record_id: int) -> Row | None:
        async with self.uow:
            result = await self.uow.repository.get_by_id(record_id)

            await self.uow.commit()
        return result

    async def delete_by_filters(self, **filters) -> None:
        async with self.uow:
            await self.uow.repository.get_by_id(**filters)
            await self.uow.commit()

    async def delete_by_id(self, record_id: int) -> int:
        async with self.uow:
            result = await self.uow.repository.delete_by_id(record_id)

            await self.uow.commit()
        return result
