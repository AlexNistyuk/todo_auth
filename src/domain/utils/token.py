from datetime import datetime, timedelta, timezone

import jwt

from infrastructure.config import get_settings

settings = get_settings()


class Token:
    def __init__(self, user_id: int = None):
        self.user_id = user_id

    def get_access_token(self):
        access_token_payload = {
            "id": self.user_id,
            "type": "access_token",
            "exp": self.__get_expire_time(
                timedelta(minutes=settings.jwt_access_token_expires_in)
            ),
        }

        return jwt.encode(
            access_token_payload, settings.jwt_secret_key, settings.jwt_algorithm
        )

    def get_refresh_token(self) -> str:
        refresh_token_payload = {
            "id": self.user_id,
            "type": "refresh_token",
            "exp": self.__get_expire_time(
                timedelta(days=settings.jwt_refresh_token_expires_in)
            ),
        }

        return jwt.encode(
            refresh_token_payload, settings.jwt_secret_key, settings.jwt_algorithm
        )

    def get_tokens(self) -> dict:
        return {
            "access_token": self.get_access_token(),
            "refresh_token": self.get_refresh_token(),
        }

    @staticmethod
    def get_payload(token: str) -> dict:
        try:
            return jwt.decode(
                token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
            )
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return {}

    @staticmethod
    def __get_expire_time(delta: timedelta) -> int:
        return int(datetime.now(tz=timezone.utc).timestamp() + delta.total_seconds())
