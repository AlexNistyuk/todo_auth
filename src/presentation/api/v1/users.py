from fastapi import APIRouter
from fastapi.params import Depends
from starlette.status import HTTP_200_OK

from application.use_cases.users import UserUseCase
from domain.entities.users import UserGetDTO
from infrastructure.permissions.users import IsAdmin, IsUserOrAdmin

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserGetDTO], status_code=HTTP_200_OK)
async def get_all_users(permission=Depends(IsAdmin())):
    return await UserUseCase().get_all()


@router.get("/{user_id}", response_model=UserGetDTO, status_code=HTTP_200_OK)
async def get_user_by_id(user_id: int, permission=Depends(IsUserOrAdmin())):
    return await UserUseCase().get_by_id(user_id)


@router.delete("/{user_id}", response_model=dict, status_code=HTTP_200_OK)
async def delete_user(user_id: int, permission=Depends(IsAdmin())):
    user_id = await UserUseCase().delete_by_id(user_id)

    return {"id": user_id}
