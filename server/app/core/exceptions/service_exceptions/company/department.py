from fastapi import status
from app.core.exceptions.service_exceptions.base import BaseAppException

class DepartmentNotFoundException(BaseAppException):
    """Raised when the department is not found."""
    def __init__(self, detail: str = "Department not found.", status_code: int = status.HTTP_404_NOT_FOUND):
        super().__init__(detail, status_code)
 