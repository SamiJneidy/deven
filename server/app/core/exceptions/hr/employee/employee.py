from fastapi import status
from app.core.exceptions.base import BaseAppException

class EmployeeNotFoundException(BaseAppException):
    """Raised when the employee is not found."""
    def __init__(self, message: str = "Employee not found.", status_code: int = status.HTTP_404_NOT_FOUND):
        super().__init__(message, status_code)

class PersonalEmailAlreadyInUseException(BaseAppException):
    """Raised when the personal email is already in use."""
    def __init__(self, message: str = "Personal email already in use.", status_code: int = status.HTTP_409_CONFLICT):
        super().__init__(message, status_code)
class WorkEmailAlreadyInUseException(BaseAppException):
    """Raised when the work email is already in use."""
    def __init__(self, message: str = "Work email already in use.", status_code: int = status.HTTP_409_CONFLICT):
        super().__init__(message, status_code)

class EmployeeEducationNotFound(BaseAppException):
    """Raised when the education is not found."""
    def __init__(self, message: str = "Education already in use.", status_code: int = status.HTTP_404_NOT_FOUND):
        super().__init__(message, status_code)

 