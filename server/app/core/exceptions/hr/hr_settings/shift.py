from fastapi import status
from server.app.core.exceptions.service_exceptions.base import BaseAppException

class ShiftNotFoundException(BaseAppException):
    """Raised when the shift is not found."""
    def __init__(self, detail: str = "Shift not found.", status_code: int = status.HTTP_404_NOT_FOUND):
        super().__init__(detail, status_code)
 