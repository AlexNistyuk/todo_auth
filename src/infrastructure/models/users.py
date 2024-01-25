import enum
from datetime import datetime
from typing import Annotated

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"


pg_enum = Annotated[str, mapped_column(PgEnum(UserRole), default=UserRole.USER)]


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(20), unique=True, index=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    role: Mapped[pg_enum]
