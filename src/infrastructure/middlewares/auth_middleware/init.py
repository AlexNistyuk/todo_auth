from dependency_injector.wiring import Provide, inject
from fastapi import FastAPI

from application.dependencies import Container
from infrastructure.middlewares.auth_middleware.middleware import AuthMiddleware


@inject
def init_auth_middleware(
    app: FastAPI,
    ignore_paths=(
        "/docs",
        "/openapi.json",
        "/api/v1/auth/register/",
        "/api/v1/auth/login/",
        "/api/v1/token/refresh/",
        "/api/v1/token/verify/",
        "/api/v1/token/user-info/",
    ),
    token_use_case=Provide[Container.token_use_case],
):
    app.add_middleware(
        AuthMiddleware, ignore_paths=ignore_paths, token_use_case=token_use_case
    )
