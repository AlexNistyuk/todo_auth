from domain.models.users import User
from infrastructure.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    """User repository. Provides operations to table users"""

    model = User
