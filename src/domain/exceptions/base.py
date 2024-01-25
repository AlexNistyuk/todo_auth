from fastapi import HTTPException


class BaseHTTPException(HTTPException):
    """Base HTTP exception"""

    status_code: int
    message: str

    def __init__(self):
        super().__init__(self.status_code, self.message)
