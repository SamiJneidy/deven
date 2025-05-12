from fastapi import status
from app.core.exceptions.base import BaseAppException

class WorkTypeNotFound(BaseAppException):
    """Raised when the work type is not found."""
    def __init__(self, message: str = "Work type not found.", status_code: int = status.HTTP_404_NOT_FOUND):
        super().__init__(message, status_code)
 