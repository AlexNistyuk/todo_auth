from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from application.use_cases.base import BaseUseCase
from domain.exceptions.exceptions import HTTP400
from domain.utils.password import Password
from infrastructure.models.users import UserRole
from infrastructure.uow.users import UserUnitOfWork


class UserUseCase(BaseUseCase):
    """Use case for UserRepository"""

    uow = UserUnitOfWork()

    async def insert(self, data: dict) -> int:
        password = data.pop("password")
        hashed_password = Password().get_hashed_password(password)

        data["password"] = hashed_password
        data["role"] = UserRole.user.value

        try:
            async with self.uow:
                result = await self.uow.repo.insert(data)

                await self.uow.commit()
        except Exception as exc:
            raise HTTP400(detail={"error": str(exc)})
        return result

    async def verify(self, credentials: dict):
        exception = HTTPException(
            detail="Incorrect username or password", status_code=HTTP_401_UNAUTHORIZED
        )

        try:
            async with self.uow:
                user = await self.uow.repo.get_by_username(credentials["username"])
        except Exception as exc:
            raise HTTP400(detail={"error": str(exc)})

        if not user:
            raise exception

        if not Password().verify(credentials["password"], user["password"]):
            raise exception
        return user
