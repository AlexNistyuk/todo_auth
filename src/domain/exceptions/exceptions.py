from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)

from domain.exceptions.base import BaseHTTPException


class HTTP400(BaseHTTPException):
    status_code = HTTP_400_BAD_REQUEST


class HTTP401(BaseHTTPException):
    status_code = HTTP_401_UNAUTHORIZED


class HTTP403(BaseHTTPException):
    status_code = HTTP_403_FORBIDDEN


class HTTP404(BaseHTTPException):
    status_code = HTTP_404_NOT_FOUND
