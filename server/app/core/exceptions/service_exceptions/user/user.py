from fastapi import status
from app.core.exceptions.service_exceptions.base import BaseAppException

class UserNotFoundException(BaseAppException):
    """Raised when the user is not found."""
    def __init__(self, detail: str = "User not found.", status_code: int = status.HTTP_404_NOT_FOUND):
        super().__init__(detail, status_code)