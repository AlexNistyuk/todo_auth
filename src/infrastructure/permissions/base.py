from fastapi import Header
from starlette.requests import Request

from application.use_cases.token import TokenUseCase
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

        async with self.uow:
            user = await self.uow.users.get_by_id(payload["id"])

        if user is None:
            raise InvalidTokenError
        return user["role"].value
