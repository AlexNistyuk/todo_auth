from typing import Any

from fastapi import HTTPException


class BaseHTTPException(HTTPException):
    status_code: int

    def __init__(self, detail: Any = None):
        super().__init__(self.status_code, detail)
