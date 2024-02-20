import datetime

from alembic import op
from sqlalchemy import Table

from domain.enums.users import UserRole
from domain.utils.password import Password
from infrastructure.config import get_settings

settings = get_settings()


def create_superuser(users: Table):
    hashed_password = Password.get_hashed_password(settings.superuser_password)

    op.bulk_insert(
        table=users,
        rows=[
            {
                "username": settings.superuser_username,
                "password": hashed_password,
                "role": UserRole.admin.value,
                "created_at": datetime.datetime.utcnow(),
                "updated_at": datetime.datetime.utcnow(),
            }
        ],
    )
