from starlette.status import HTTP_401_UNAUTHORIZED

from domain.exceptions.base import BaseHTTPException


class InvalidTokenError(BaseHTTPException):
    status_code = HTTP_401_UNAUTHORIZED
    message = "Invalid token"


class InvalidAuthHeaderDataError(BaseHTTPException):
    status_code = HTTP_401_UNAUTHORIZED
    message = "Invalid authorization header data"
