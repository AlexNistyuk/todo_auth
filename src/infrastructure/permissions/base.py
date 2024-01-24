from fastapi import Header
from sqlalchemy.exc import NoResultFound
from starlette.requests import Request

from application.use_cases.token import TokenUseCase
from domain.exceptions.exceptions import HTTP400, HTTP401, HTTP403
from infrastructure.permissions.interfaces import IPermission
from infrastructure.uow.users import UserUnitOfWork


class BasePermission(IPermission):
    """Base permission"""

    uow = UserUnitOfWork()
    token_use_case = TokenUseCase()

    def __init__(self):
        self.user = None

    async def __call__(self, request: Request):
        user_role = await self.__get_user_role(request.headers)

        result = await self.has_permission(user_role)
        if not result:
            raise HTTP403
        return self

    async def __get_user_role(self, headers: Header) -> str:
        payload = await self.token_use_case.verify(headers)

        try:
            async with self.uow:
                self.user = await self.uow.repo.get_by_id(payload["id"])
        except NoResultFound:
            raise HTTP401(detail="Invalid token")
        except Exception as exc:
            raise HTTP400(detail={"error": str(exc)})

        return self.user["role"].value
