from app.core.exceptions.base import BaseAppException
from fastapi import status

class UserNotFoundException(BaseAppException):
    """Raised when the user is not found."""
    def __init__(self, message: str = "User not found.", status_code: int = status.HTTP_404_NOT_FOUND):
        super().__init__(message, status_code)