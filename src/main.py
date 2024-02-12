from contextlib import asynccontextmanager

from fastapi import FastAPI

from infrastructure.managers.database import DatabaseManager
from presentation.routers import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_manager = await DatabaseManager.connect()

    yield

    await db_manager.close()


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
