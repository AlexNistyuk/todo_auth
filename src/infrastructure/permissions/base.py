from fastapi import Header
from starlette.requests import Request

from application.use_cases.token import TokenUseCase
from domain.exceptions.repositories import (
    RepositoryNotFoundError,
    RepositoryUnknownError,
)
from domain.exceptions.token import InvalidTokenError
from domain.exceptions.users import UserPermissionDenied
from infrastructure.permissions.interfaces import IPermission
from infrastructure.uow.base import UnitOfWork


class BasePermission(IPermission):
    """Base permission"""

    uow = UnitOfWork()
    token_use_case = TokenUseCase

    async def __call__(self, request: Request):
        user_role = await self.__get_user_role(request.headers)

        result = await self.has_permission(user_role)
        if not result:
            raise UserPermissionDenied
        return self

    async def __get_user_role(self, headers: Header) -> str:
        payload = await self.token_use_case.verify(headers)

        user_id = payload.get("id")
        if user_id is None:
            raise InvalidTokenError

        try:
            async with self.uow(autocommit=True):
                user = await self.uow.users.get_by_id(user_id)
        except RepositoryNotFoundError:
            raise InvalidTokenError
        except RepositoryUnknownError:
            raise InvalidTokenError
        return user.role.value
