from fastapi import status
from app.core.exceptions.service_exceptions.base import BaseAppException

class EmployeeEducationNotFoundException(BaseAppException):
    """Raised when the education is not found."""
    def __init__(self, detail: str = "Education already in use.", status_code: int = status.HTTP_404_NOT_FOUND):
        super().__init__(detail, status_code)
 