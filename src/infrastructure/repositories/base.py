from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

from infrastructure.repositories.interfaces import IRepository


class BaseRepository(IRepository):
    """Base repository"""

    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert(self, data: dict) -> int:
        query = insert(self.model).values(**data).returning(self.model.id)
        result = await self.session.execute(query)

        return result.scalar_one()

    async def update_by_filters(self, data: dict, **filters) -> None:
        query = update(self.model).values(**data).filter_by(**filters)
        await self.session.execute(query)

    async def update_by_id(self, data: dict, record_id: int) -> int:
        query = (
            update(self.model)
            .values(**data)
            .filter_by(id=record_id)
            .returning(self.model.id)
        )
        result = await self.session.execute(query)

        return result.scalar_one()

    async def get_by_filters(self, **filters) -> Sequence:
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)

        return result.scalars().all()

    async def get_all(self) -> list[dict]:
        query = select(self.model)
        result = await self.session.execute(query)

        return [item.__dict__ for item in result.scalars().all()]

    async def get_by_id(self, record_id: int) -> dict:
        query = select(self.model).filter_by(id=record_id)
        result = await self.session.execute(query)

        try:
            return result.scalar_one().__dict__
        except NoResultFound:
            raise HTTPException(detail="Not found", status_code=HTTP_404_NOT_FOUND)

    async def get_by_username(self, username: str) -> dict:
        query = select(self.model).filter_by(username=username)
        result = await self.session.execute(query)

        try:
            return result.scalar_one().__dict__
        except NoResultFound:
            raise HTTPException(detail="Not found", status_code=HTTP_404_NOT_FOUND)

    async def delete_by_filters(self, **filters) -> None:
        query = delete(self.model).filter_by(**filters)
        await self.session.execute(query)

    async def delete_by_id(self, record_id: int) -> int:
        query = delete(self.model).filter_by(id=record_id).returning(self.model.id)
        result = await self.session.execute(query)

        try:
            return result.scalar_one()
        except NoResultFound:
            raise HTTPException(detail="Not found", status_code=HTTP_404_NOT_FOUND)
