from fastapi import status
from app.core.exceptions.base import BaseAppException

class LocationNotFoundException(BaseAppException):
    """Raised when the location is not found."""
    def __init__(self, message: str = "Location not found.", status_code: int = status.HTTP_404_NOT_FOUND):
        super().__init__(message, status_code)
 