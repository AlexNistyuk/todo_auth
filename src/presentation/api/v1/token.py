from fastapi import APIRouter
from starlette.requests import Request
from starlette.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from application.use_cases.token import TokenUseCase
from application.use_cases.users import UserUseCase
from domain.entities.token import TokenDTO
from domain.entities.users import UserRetrieveDTO

router = APIRouter()


@router.post(
    "/refresh",
    response_model=TokenDTO,
    status_code=HTTP_200_OK,
    responses={HTTP_401_UNAUTHORIZED: {}, HTTP_400_BAD_REQUEST: {}},
)
async def get_new_tokens(refresh_token: str):
    return await TokenUseCase.get_new_tokens(refresh_token)


@router.get(
    "/verify", status_code=HTTP_204_NO_CONTENT, responses={HTTP_401_UNAUTHORIZED: {}}
)
async def verify_token(request: Request):
    await TokenUseCase.verify(request.headers)


@router.get(
    "/user-info",
    response_model=UserRetrieveDTO,
    status_code=HTTP_200_OK,
    responses={HTTP_401_UNAUTHORIZED: {}, HTTP_400_BAD_REQUEST: {}},
)
async def get_user_info(request: Request):
    payload = await TokenUseCase.verify(request.headers)

    return await UserUseCase().get_by_id(payload.get("id"))
