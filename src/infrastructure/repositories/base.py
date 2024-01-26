from typing import Sequence

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from domain.exceptions.repositories import (
    RepositoryIntegrityError,
    RepositoryNotFoundError,
    RepositoryUnknownError,
)
from infrastructure.repositories.interfaces import IRepository


class BaseRepository(IRepository):
    """Base repository"""

    model = None

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def insert(self, data: dict) -> int | None:
        try:
            query = insert(self.model).values(**data).returning(self.model.id)
            executor = await self.session.execute(query)

            return executor.scalar_one()
        except IntegrityError:
            raise RepositoryIntegrityError
        except Exception:
            raise RepositoryUnknownError

    async def update_by_filters(self, data: dict, **filters) -> None:
        try:
            query = update(self.model).values(**data).filter_by(**filters)
            await self.session.execute(query)
        except NoResultFound:
            raise RepositoryNotFoundError
        except IntegrityError:
            raise RepositoryIntegrityError
        except Exception:
            raise RepositoryUnknownError

    async def update_by_id(self, data: dict, record_id: int) -> int | None:
        try:
            query = (
                update(self.model)
                .values(**data)
                .filter_by(id=record_id)
                .returning(self.model.id)
            )
            executor = await self.session.execute(query)

            return executor.scalar_one()
        except NoResultFound:
            raise RepositoryNotFoundError
        except IntegrityError:
            raise RepositoryIntegrityError
        except Exception:
            raise RepositoryUnknownError

    async def get_by_filters(self, **filters) -> Sequence | None:
        try:
            query = select(self.model).filter_by(**filters)
            executor = await self.session.execute(query)

            result = executor.scalars().all()
            if not result:
                raise RepositoryNotFoundError
            return result
        except NoResultFound:
            raise RepositoryNotFoundError
        except Exception:
            raise RepositoryUnknownError

    async def get_all(self) -> Sequence | None:
        try:
            query = select(self.model)
            executor = await self.session.execute(query)

            result = executor.scalars().all()
            if not result:
                raise RepositoryNotFoundError
            return result
        except NoResultFound:
            raise RepositoryNotFoundError
        except Exception:
            raise RepositoryUnknownError

    async def get_by_id(self, record_id: int) -> dict | None:
        try:
            query = select(self.model).filter_by(id=record_id)
            executor = await self.session.execute(query)

            return executor.scalar_one()
        except NoResultFound:
            raise RepositoryNotFoundError
        except Exception:
            raise RepositoryUnknownError

    async def delete_by_filters(self, **filters) -> None:
        try:
            query = delete(self.model).filter_by(**filters)
            await self.session.execute(query)
        except NoResultFound:
            raise RepositoryNotFoundError
        except Exception:
            raise RepositoryUnknownError

    async def delete_by_id(self, record_id: int) -> int | None:
        try:
            query = delete(self.model).filter_by(id=record_id).returning(self.model.id)
            executor = await self.session.execute(query)

            return executor.scalar_one()
        except NoResultFound:
            raise RepositoryNotFoundError
        except Exception:
            raise RepositoryUnknownError
