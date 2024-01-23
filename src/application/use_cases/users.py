from sqlalchemy.exc import NoResultFound

from application.use_cases.base import BaseUseCase
from domain.exceptions.exceptions import HTTP400, HTTP401
from domain.utils.password import Password
from infrastructure.models.users import UserRole
from infrastructure.uow.users import UserUnitOfWork


class UserUseCase(BaseUseCase):
    """Use case for UserUnitOfWork"""

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
        try:
            async with self.uow:
                user = await self.uow.repo.get_by_username(credentials["username"])
        except NoResultFound:
            raise HTTP401(detail="Incorrect username or password")
        except Exception as exc:
            raise HTTP400(detail={"error": str(exc)})

        if not Password().verify(credentials["password"], user["password"]):
            raise HTTP401(detail="Incorrect username or password")
        return user
