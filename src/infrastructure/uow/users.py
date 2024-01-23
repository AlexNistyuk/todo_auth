from infrastructure.repositories.users import UserRepository
from infrastructure.uow.base import BaseUnitOfWork


class UserUnitOfWork(BaseUnitOfWork):
    """Unit of work for users repository"""

    repository = UserRepository
