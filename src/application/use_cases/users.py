from application.use_cases.base import BaseUseCase
from infrastructure.repositories.users import UserRepository


class UserUseCase(BaseUseCase):
    """Use case for UserRepository"""

    repository = UserRepository
