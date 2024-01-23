from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from domain.exceptions.base import BaseHTTPException


class HTTP400(BaseHTTPException):
    status_code = HTTP_400_BAD_REQUEST


class HTTP401(BaseHTTPException):
    status_code = HTTP_401_UNAUTHORIZED
