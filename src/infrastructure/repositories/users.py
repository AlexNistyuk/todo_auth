from sqlalchemy import select

from infrastructure.models.users import User
from infrastructure.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    """User repository. Provides operations to table users"""

    model = User

    async def get_by_username(self, username: str) -> User | None:
        try:
            query = select(self.model).filter_by(username=username)
            result = await self.session.execute(query)

            return result.scalar_one()
        except Exception:
            return
