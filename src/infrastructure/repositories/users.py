from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from domain.exceptions.repositories import (
    RepositoryNotFoundError,
    RepositoryUnknownError,
)
from infrastructure.models.users import User
from infrastructure.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    """User repository. Provides operations to table users"""

    model = User

    async def get_by_username(self, username: str) -> User:
        try:
            query = select(self.model).filter_by(username=username)
            executor = await self.session.execute(query)

            return executor.scalar_one()
        except NoResultFound:
            raise RepositoryNotFoundError
        except Exception:
            raise RepositoryUnknownError
