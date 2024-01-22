from fastapi import APIRouter

from domain.entities.users import UserGetDTO

router = APIRouter(prefix="/auth/users", tags=["Auth"])


@router.get("/", response_model=list[UserGetDTO])
async def get_all_users():
    ...
