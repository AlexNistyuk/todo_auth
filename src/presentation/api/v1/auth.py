from fastapi import APIRouter
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from application.use_cases.users import UserUseCase
from domain.entities.auth import AuthLoginDTO
from domain.entities.token import TokenDTO
from domain.entities.users import UserCreateDTO
from domain.utils.token import Token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenDTO, status_code=HTTP_200_OK)
async def login(credentials: AuthLoginDTO):
    user_data = await UserUseCase().verify(credentials.model_dump())

    return Token(user_data["id"]).get_tokens()


@router.post("/register", response_model=dict, status_code=HTTP_201_CREATED)
async def create_user(new_user: UserCreateDTO):
    user_id = await UserUseCase().insert(new_user.model_dump())

    return {"id": user_id}
