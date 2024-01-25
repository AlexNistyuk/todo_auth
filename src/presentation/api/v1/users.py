from fastapi import APIRouter
from fastapi.params import Depends
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from application.use_cases.users import UserUseCase
from domain.entities.users import UserRetrieveDTO
from infrastructure.permissions.users import IsAdmin, IsUserOrAdmin

router = APIRouter()


@router.get("/", response_model=list[UserRetrieveDTO], status_code=HTTP_200_OK)
async def get_all_users(permission=Depends(IsAdmin())):
    return await UserUseCase().get_all()


@router.get("/{user_id}", response_model=UserRetrieveDTO, status_code=HTTP_200_OK)
async def get_user_by_id(user_id: int, permission=Depends(IsUserOrAdmin())):
    return await UserUseCase().get_by_id(user_id)


@router.delete("/{user_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, permission=Depends(IsAdmin())):
    await UserUseCase().delete_by_id(user_id)
