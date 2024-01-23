from fastapi import APIRouter

from presentation.api.v1.auth import router as auth_router
from presentation.api.v1.token import router as token_router
from presentation.api.v1.users import router as users_router

router = APIRouter(prefix="/v1", tags=["v1"])
router.include_router(users_router)
router.include_router(auth_router)
router.include_router(token_router)
