from datetime import datetime

from pydantic import BaseModel


class UserCreateDTO(BaseModel):
    username: str
    password: str


class UserIdDTO(BaseModel):
    id: int


class UserRetrieveDTO(UserIdDTO):
    username: str
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
