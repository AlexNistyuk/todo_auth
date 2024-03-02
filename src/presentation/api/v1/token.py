from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from application.dependencies import Container
from domain.entities.token import TokenDTO
from domain.entities.users import UserRetrieveDTO

router = APIRouter()


@router.post(
    "/refresh/",
    response_model=TokenDTO,
    status_code=HTTP_200_OK,
    responses={HTTP_401_UNAUTHORIZED: {}, HTTP_400_BAD_REQUEST: {}},
)
@inject
async def get_new_tokens(
    refresh_token: str, token_use_case=Depends(Provide[Container.token_use_case])
):
    return await token_use_case.get_new_tokens(refresh_token)


@router.get(
    "/verify/", status_code=HTTP_204_NO_CONTENT, responses={HTTP_401_UNAUTHORIZED: {}}
)
@inject
async def verify_token(
    request: Request, token_use_case=Depends(Provide[Container.token_use_case])
):
    await token_use_case.verify(request.headers)


@router.get(
    "/user-info/",
    response_model=UserRetrieveDTO,
    status_code=HTTP_200_OK,
    responses={HTTP_401_UNAUTHORIZED: {}, HTTP_400_BAD_REQUEST: {}},
)
@inject
async def get_user_info(
    request: Request, token_use_case=Depends(Provide[Container.token_use_case])
):
    return await token_use_case.get_user_info(request.headers)
