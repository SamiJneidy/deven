from fastapi import status
from .base_exceptions import BaseAppException

class UserNotActiveError(BaseAppException):
    """Raised when the user is not active."""
    def __init__(self, message: str = "User is not active", status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(message, status_code)