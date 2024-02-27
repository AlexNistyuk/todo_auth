from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from application.dependencies import Container
from domain.entities.auth import AuthLoginDTO
from domain.entities.token import TokenDTO
from domain.entities.users import UserCreateDTO, UserIdDTO
from domain.utils.token import Token

router = APIRouter()


@router.post(
    "/login",
    response_model=TokenDTO,
    status_code=HTTP_200_OK,
    responses={HTTP_401_UNAUTHORIZED: {}},
)
@inject
async def login(
    credentials: AuthLoginDTO, user_use_case=Depends(Provide[Container.user_use_case])
):
    user = await user_use_case.verify(credentials.model_dump())

    return Token(user.id).get_tokens()


@router.post(
    "/register",
    response_model=UserIdDTO,
    status_code=HTTP_201_CREATED,
    responses={HTTP_401_UNAUTHORIZED: {}, HTTP_400_BAD_REQUEST: {}},
)
@inject
async def create_user(
    new_user: UserCreateDTO, user_use_case=Depends(Provide[Container.user_use_case])
):
    user_id = await user_use_case.insert(new_user.model_dump())

    return {"id": user_id}
