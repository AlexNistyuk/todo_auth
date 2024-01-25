from passlib.context import CryptContext


class Password:
    """Hash and verify password"""

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def get_hashed_password(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    def verify(cls, password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(password, hashed_password)
