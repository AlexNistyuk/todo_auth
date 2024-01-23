from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from application.use_cases.users import UserUseCase
from domain.entities.token import TokenDTO
from domain.entities.users import UserGetDTO
from domain.utils.token import Token

router = APIRouter(prefix="/token", tags=["Token"])


@router.get("/refresh", response_model=TokenDTO, status_code=HTTP_200_OK)
async def get_new_tokens(refresh_token: str):
    try:
        payload = Token().get_payload(refresh_token)
        if payload.get("type") != "refresh_token":
            raise HTTPException(
                detail="Invalid token", status_code=HTTP_400_BAD_REQUEST
            )

        user_data = await UserUseCase().get_by_id(payload["id"])
        user = UserGetDTO(**user_data)

        return Token(user).get_tokens()
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            detail={"error": str(exc)}, status_code=HTTP_400_BAD_REQUEST
        )
