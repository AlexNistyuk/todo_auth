from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter
from fastapi.params import Depends
from starlette.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from application.dependencies import Container
from domain.entities.users import UserRetrieveDTO
from infrastructure.permissions.users import IsAdmin, IsUserOrAdmin

router = APIRouter()


@router.get(
    "/",
    response_model=list[UserRetrieveDTO],
    status_code=HTTP_200_OK,
    responses={HTTP_401_UNAUTHORIZED: {}, HTTP_400_BAD_REQUEST: {}},
)
@inject
async def get_all_users(
    permission=Depends(IsAdmin()),
    user_use_case=Depends(Provide[Container.user_use_case]),
):
    return await user_use_case.get_all()


@router.get(
    "/{user_id}",
    response_model=UserRetrieveDTO,
    status_code=HTTP_200_OK,
    responses={HTTP_401_UNAUTHORIZED: {}, HTTP_400_BAD_REQUEST: {}},
)
@inject
async def get_user_by_id(
    user_id: int,
    permission=Depends(IsUserOrAdmin()),
    user_use_case=Depends(Provide[Container.user_use_case]),
):
    return await user_use_case.get_by_id(user_id)


@router.delete(
    "/{user_id}",
    status_code=HTTP_204_NO_CONTENT,
    responses={HTTP_401_UNAUTHORIZED: {}, HTTP_400_BAD_REQUEST: {}},
)
@inject
async def delete_user(
    user_id: int,
    permission=Depends(IsAdmin()),
    user_use_case=Depends(Provide[Container.user_use_case]),
):
    await user_use_case.delete_by_id(user_id)
