from sqlalchemy import Sequence

from application.use_cases.interfaces import IUseCase
from domain.exceptions.repositories import (
    RepositoryIntegrityError,
    RepositoryNotFoundError,
    RepositoryUnknownError,
)
from domain.exceptions.users import (
    UserDeleteError,
    UserIncorrectCredentialsError,
    UserInsertError,
    UserNotFoundError,
    UserNotUniqueData,
    UserRetrieveError,
    UserUpdateError,
    UserVerifyError,
)
from domain.utils.password import Password
from infrastructure.models.users import User
from infrastructure.uow.base import UnitOfWork


class UserUseCase(IUseCase):
    """Use case for UserUnitOfWork"""

    uow = UnitOfWork()

    async def insert(self, data: dict) -> int:
        password = data.pop("password")
        hashed_password = Password.get_hashed_password(password)

        data["password"] = hashed_password

        try:
            async with self.uow(autocommit=True):
                result = await self.uow.users.insert(data)
        except RepositoryIntegrityError:
            raise UserNotUniqueData
        except RepositoryUnknownError:
            raise UserInsertError
        return result

    async def update_by_filters(self, data: dict, **filters) -> None:
        try:
            async with self.uow(autocommit=True):
                await self.uow.users.update_by_filters(data, **filters)
        except RepositoryNotFoundError:
            raise UserNotFoundError
        except RepositoryIntegrityError:
            raise UserNotUniqueData
        except RepositoryUnknownError:
            raise UserUpdateError

    async def update_by_id(self, data: dict, record_id: int) -> int:
        try:
            async with self.uow(autocommit=True):
                result = await self.uow.users.update_by_id(data, record_id)
        except RepositoryNotFoundError:
            raise UserNotFoundError
        except RepositoryIntegrityError:
            raise UserNotUniqueData
        except RepositoryUnknownError:
            raise UserUpdateError
        return result

    async def get_by_filters(self, **filters) -> Sequence[User]:
        try:
            async with self.uow(autocommit=True):
                result = await self.uow.users.get_by_filters(**filters)
        except RepositoryNotFoundError:
            raise UserNotFoundError
        except RepositoryUnknownError:
            raise UserRetrieveError
        return result

    async def get_all(self) -> Sequence[User]:
        try:
            async with self.uow(autocommit=True):
                result = await self.uow.users.get_all()
        except RepositoryNotFoundError:
            raise UserNotFoundError
        except RepositoryUnknownError:
            raise UserRetrieveError
        return result

    async def get_by_id(self, record_id: int) -> User:
        try:
            async with self.uow(autocommit=True):
                result = await self.uow.users.get_by_id(record_id)
        except RepositoryNotFoundError:
            raise UserNotFoundError
        except RepositoryUnknownError:
            raise UserRetrieveError
        return result

    async def delete_by_filters(self, **filters) -> None:
        try:
            async with self.uow(autocommit=True):
                await self.uow.users.get_by_id(**filters)
        except RepositoryNotFoundError:
            raise UserNotFoundError
        except RepositoryUnknownError:
            raise UserDeleteError

    async def delete_by_id(self, record_id: int) -> None:
        try:
            async with self.uow(autocommit=True):
                await self.uow.users.delete_by_id(record_id)
        except RepositoryNotFoundError:
            raise UserNotFoundError
        except RepositoryUnknownError:
            raise UserDeleteError

    async def verify(self, credentials: dict) -> User:
        try:
            async with self.uow(autocommit=True):
                user = await self.uow.users.get_by_username(credentials["username"])
        except RepositoryNotFoundError:
            raise UserIncorrectCredentialsError
        except RepositoryUnknownError:
            raise UserVerifyError

        if not Password.verify(credentials["password"], user.password):
            raise UserIncorrectCredentialsError
        return user
