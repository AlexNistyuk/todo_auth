import datetime

from pydantic import BaseModel


class UserCreateDTO(BaseModel):
    username: str
    password: str


class UserGetDTO(BaseModel):
    id: int
    username: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
