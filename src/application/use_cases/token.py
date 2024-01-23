from typing import Any

from fastapi import HTTPException
from starlette.datastructures import Headers
from starlette.status import HTTP_400_BAD_REQUEST

from application.use_cases.users import UserUseCase
from domain.exceptions.exceptions import HTTP401
from domain.utils.token import Token
from infrastructure.config import get_settings

settings = get_settings()


class TokenUseCase:
    async def get_new_tokens(self, refresh_token: str) -> dict:
        payload = Token().get_payload(refresh_token)
        if payload.get("type") != "refresh_token":
            raise HTTPException(
                detail="Invalid token", status_code=HTTP_400_BAD_REQUEST
            )

        user_data = await UserUseCase().get_by_id(payload["id"])

        return Token(user_data["id"]).get_tokens()

    def __raise_unauthorized_exception(self, message: Any):
        raise HTTP401(detail=message)

    async def verify(self, headers: Headers) -> None:
        header_list = headers.get(settings.http_auth_header, "").split()

        if len(header_list) != 2:
            self.__raise_unauthorized_exception("Invalid auth data")

        if header_list[0] != settings.http_auth_keyword:
            self.__raise_unauthorized_exception("Invalid auth data")

        payload = Token().get_payload(header_list[1])
        if payload.get("type") != "access_token":
            self.__raise_unauthorized_exception("Invalid token")
