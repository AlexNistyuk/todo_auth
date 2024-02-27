from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
)

from domain.exceptions.base import BaseHTTPException


class UserNotUniqueData(BaseHTTPException):
    status_code = HTTP_400_BAD_REQUEST
    message = "Provided data not unique"


class UserNotFoundError(BaseHTTPException):
    status_code = HTTP_400_BAD_REQUEST
    message = "User not found error"


class UserInsertError(BaseHTTPException):
    status_code = HTTP_400_BAD_REQUEST
    message = "Error while inserting user"


class UserUpdateError(BaseHTTPException):
    status_code = HTTP_400_BAD_REQUEST
    message = "Error with updating user"


class UserRetrieveError(BaseHTTPException):
    status_code = HTTP_400_BAD_REQUEST
    message = "Error while retrieving user"


class UserDeleteError(BaseHTTPException):
    status_code = HTTP_400_BAD_REQUEST
    message = "Error while deleting user"


class UserIncorrectCredentialsError(BaseHTTPException):
    status_code = HTTP_401_UNAUTHORIZED
    message = "Incorrect credentials"


class UserVerifyError(BaseHTTPException):
    status_code = HTTP_401_UNAUTHORIZED
    message = "Error while user verification"


class UserPermissionDenied(BaseHTTPException):
    status_code = HTTP_403_FORBIDDEN
    message = "Permission denied"
