from fastapi import status
from app.core.exceptions.base import BaseAppException

class ShiftNotFoundException(BaseAppException):
    """Raised when the shift is not found."""
    def __init__(self, message: str = "Shift not found.", status_code: int = status.HTTP_404_NOT_FOUND):
        super().__init__(message, status_code)
 