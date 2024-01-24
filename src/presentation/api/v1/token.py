from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_200_OK

from application.use_cases.token import TokenUseCase
from application.use_cases.users import UserUseCase
from domain.entities.token import TokenDTO
from domain.entities.users import UserGetDTO

router = APIRouter(prefix="/token", tags=["Token"])


@router.post("/refresh", response_model=TokenDTO, status_code=HTTP_200_OK)
async def get_new_tokens(refresh_token: str):
    return await TokenUseCase().get_new_tokens(refresh_token)


@router.get("/verify", status_code=HTTP_200_OK)
async def verify_token(request: Request):
    await TokenUseCase().verify(request.headers)

    return Response(content="valid")


@router.get("/user-info", response_model=UserGetDTO, status_code=HTTP_200_OK)
async def get_user_info(request: Request):
    payload = await TokenUseCase().verify(request.headers)

    return await UserUseCase().get_by_id(payload["id"])
