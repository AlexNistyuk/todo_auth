from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from infrastructure.managers.database import DatabaseManager
from presentation.api.routers import router as v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_manager = await DatabaseManager.connect()

    yield

    await db_manager.close()


app = FastAPI(lifespan=lifespan)
app.include_router(v1_router)


if __name__ == "__main__":
    uvicorn.run(app=app, host="localhost", port=8000)
