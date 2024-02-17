from starlette.datastructures import Headers

from application.use_cases.interfaces import IUseCase
from domain.exceptions.token import InvalidAuthHeaderDataError, InvalidTokenError
from domain.utils.token import Token
from infrastructure.config import get_settings
from infrastructure.models.users import User

settings = get_settings()


class TokenUseCase:
    """Use case for working with token"""

    def __init__(self, user_use_case: IUseCase) -> None:
        self.user_use_case = user_use_case

    async def get_new_tokens(self, refresh_token: str) -> dict:
        payload = Token.get_payload(refresh_token)
        if payload.get("type") != "refresh_token":
            raise InvalidTokenError

        user_id = payload.get("id")
        if user_id is None:
            raise InvalidTokenError

        user = await self.user_use_case.get_by_id(user_id)

        return Token(user.id).get_tokens()

    async def verify(self, headers: Headers) -> dict:
        header_list = headers.get(settings.http_auth_header, "").split()

        if len(header_list) != 2:
            raise InvalidAuthHeaderDataError

        if header_list[0] != settings.http_auth_keyword:
            raise InvalidAuthHeaderDataError

        payload = Token.get_payload(header_list[1])
        if payload.get("type") != "access_token":
            raise InvalidTokenError
        return payload

    async def get_user_info(self, headers: Headers) -> User:
        payload = await self.verify(headers)

        return await self.user_use_case.get_by_id(payload.get("id"))
