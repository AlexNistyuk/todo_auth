from typing import Sequence

from application.use_cases.interfaces import IUseCase
from domain.exceptions.exceptions import HTTP400
from infrastructure.uow.interfaces import IUnitOfWork


class BaseUseCase(IUseCase):
    """Base use case"""

    uow: IUnitOfWork

    async def insert(self, data: dict) -> int:
        try:
            async with self.uow:
                result = await self.uow.repository.insert(data)

                await self.uow.commit()
        except Exception as exc:
            raise HTTP400(detail={"error": str(exc)})
        return result

    async def update_by_filters(self, data: dict, **filters) -> None:
        try:
            async with self.uow:
                await self.uow.repository.update_by_filters(data, **filters)
                await self.uow.commit()
        except Exception as exc:
            raise HTTP400(detail={"error": str(exc)})

    async def update_by_id(self, data: dict, record_id: int) -> int:
        try:
            async with self.uow:
                result = await self.uow.repository.update_by_id(data, record_id)

                await self.uow.commit()
        except Exception as exc:
            raise HTTP400(detail={"error": str(exc)})
        return result

    async def get_by_filters(self, **filters) -> Sequence:
        try:
            async with self.uow:
                return await self.uow.repository.get_by_filters(**filters)
        except Exception as exc:
            raise HTTP400(detail={"error": str(exc)})

    async def get_all(self) -> Sequence:
        try:
            async with self.uow:
                return await self.uow.repository.get_all()
        except Exception as exc:
            raise HTTP400(detail={"error": str(exc)})

    async def get_by_id(self, record_id: int) -> dict:
        try:
            async with self.uow:
                return await self.uow.repository.get_by_id(record_id)
        except Exception as exc:
            raise HTTP400(detail={"error": str(exc)})

    async def delete_by_filters(self, **filters) -> None:
        try:
            async with self.uow:
                await self.uow.repository.get_by_id(**filters)
                await self.uow.commit()
        except Exception as exc:
            raise HTTP400(detail={"error": str(exc)})

    async def delete_by_id(self, record_id: int) -> int:
        try:
            async with self.uow:
                result = await self.uow.repository.delete_by_id(record_id)

                await self.uow.commit()
        except Exception as exc:
            raise HTTP400(detail={"error": str(exc)})
        return result
