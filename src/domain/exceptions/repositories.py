from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from domain.exceptions.base import BaseHTTPException


class RepositoryUnknownError(BaseHTTPException):
    status_code = HTTP_400_BAD_REQUEST
    message = "Unknown error"


class RepositoryIntegrityError(BaseHTTPException):
    status_code = HTTP_400_BAD_REQUEST
    message = "Integrity error"


class RepositoryNotFoundError(BaseHTTPException):
    status_code = HTTP_404_NOT_FOUND
    message = "Integrity error"
