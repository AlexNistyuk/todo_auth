from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from application.use_cases.base import BaseUseCase
from domain.utils.password import Password
from infrastructure.repositories.users import UserRepository


class UserUseCase(BaseUseCase):
    """Use case for UserRepository"""

    repository = UserRepository

    async def insert(self, data: dict) -> int:
        password = data.pop("password")
        hashed_password = Password().get_hashed_password(password)

        data["password"] = hashed_password

        async with self.uow:
            result = await self.uow.repository.insert(data)

            await self.uow.commit()
        return result

    async def verify(self, credentials: dict):
        exception = HTTPException(
            detail="Incorrect username or password", status_code=HTTP_401_UNAUTHORIZED
        )

        async with self.uow:
            user = await self.uow.repository.get_by_username(credentials["username"])

        if not user:
            raise exception

        if not Password().verify(credentials["password"], user["password"]):
            raise exception
        return user
