from starlette.datastructures import Headers

from application.use_cases.users import UserUseCase
from domain.exceptions.token import InvalidAuthHeaderDataError, InvalidTokenError
from domain.utils.token import Token
from infrastructure.config import get_settings

settings = get_settings()


class TokenUseCase:
    """Use case for working with token"""

    @classmethod
    async def get_new_tokens(cls, refresh_token: str) -> dict:
        payload = Token.get_payload(refresh_token)
        if payload.get("type") != "refresh_token":
            raise InvalidTokenError

        user_id = payload.get("id")
        if user_id is None:
            raise InvalidTokenError

        user = await UserUseCase().get_by_id(user_id)

        return Token(user.id).get_tokens()

    @classmethod
    async def verify(cls, headers: Headers) -> dict:
        header_list = headers.get(settings.http_auth_header, "").split()

        if len(header_list) != 2:
            raise InvalidAuthHeaderDataError

        if header_list[0] != settings.http_auth_keyword:
            raise InvalidAuthHeaderDataError

        payload = Token.get_payload(header_list[1])
        if payload.get("type") != "access_token":
            raise InvalidTokenError
        return payload
