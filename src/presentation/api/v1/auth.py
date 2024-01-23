from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from application.use_cases.users import UserUseCase
from domain.entities.auth import AuthLoginDTO
from domain.entities.token import TokenDTO
from domain.entities.users import UserCreateDTO, UserGetDTO
from domain.utils.token import Token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenDTO, status_code=HTTP_200_OK)
async def login(credentials: AuthLoginDTO):
    try:
        user_data = await UserUseCase().verify(credentials.model_dump())
        user = UserGetDTO(**user_data)

        return Token(user).get_tokens()
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            detail={"error": str(exc)}, status_code=HTTP_400_BAD_REQUEST
        )


@router.post("/register", response_model=dict, status_code=HTTP_201_CREATED)
async def create_user(new_user: UserCreateDTO):
    try:
        user_id = await UserUseCase().insert(new_user.model_dump())

        return {"id": user_id}
    except Exception as exc:
        raise HTTPException(
            detail={"error": str(exc)}, status_code=HTTP_400_BAD_REQUEST
        )
