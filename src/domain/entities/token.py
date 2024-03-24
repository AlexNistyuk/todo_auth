from pydantic import BaseModel


class TokenRefreshDTO(BaseModel):
    refresh_token: str


class TokenDTO(TokenRefreshDTO):
    access_token: str
