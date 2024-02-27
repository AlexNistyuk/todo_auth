from datetime import datetime

from pydantic import BaseModel, Field


class UserCreateDTO(BaseModel):
    username: str = Field(min_length=5, max_length=20)
    password: str = Field(min_length=5, max_length=15)


class UserIdDTO(BaseModel):
    id: int


class UserRetrieveDTO(UserIdDTO):
    username: str
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
