from fastapi import APIRouter

from presentation.api.routers import router as api_router

router = APIRouter(prefix="/api", tags=["API"])

router.include_router(api_router)
