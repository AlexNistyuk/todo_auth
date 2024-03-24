from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from infrastructure.config import get_settings

settings = get_settings()


def init_cors_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,
        allow_credentials=settings.allow_credentials,
        allow_methods=settings.allow_methods,
        allow_headers=settings.allow_headers,
    )
