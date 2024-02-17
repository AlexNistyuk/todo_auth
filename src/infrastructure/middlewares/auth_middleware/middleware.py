import typing

from starlette.middleware.base import (
    BaseHTTPMiddleware,
    DispatchFunction,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from application.use_cases.token import TokenUseCase


class AuthMiddleware(BaseHTTPMiddleware):
    """Set current user to request"""

    def __init__(
        self,
        app: ASGIApp,
        ignore_paths: tuple,
        token_use_case: TokenUseCase,
        dispatch: typing.Optional[DispatchFunction] = None,
    ):
        super().__init__(app, dispatch)
        self.ignore_paths = ignore_paths
        self.token_use_case = token_use_case

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        if request.url.path not in self.ignore_paths:
            try:
                user = await self.token_use_case.get_user_info(request.headers)
            except Exception:
                user = None

            if not user:
                return Response(status_code=401)

            request.state.user = user

        return await call_next(request)
