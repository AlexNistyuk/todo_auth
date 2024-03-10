from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from application.dependencies import Container
from infrastructure.managers.database import DatabaseManager
from infrastructure.middlewares.auth_middleware.init import init_auth_middleware
from presentation.routers import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await DatabaseManager.connect()

    yield

    await DatabaseManager.close()


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

container = Container()
container.wire(
    modules=[
        "presentation.api.v1.auth",
        "presentation.api.v1.token",
        "presentation.api.v1.users",
        "infrastructure.middlewares.auth_middleware.init",
    ]
)

# TODO make a function like init_auth_middleware

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


init_auth_middleware(app)
