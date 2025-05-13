from fastapi import status
from app.core.exceptions.base import BaseAppException

class JobTitleNotFound(BaseAppException):
    """Raised when the job title is not found."""
    def __init__(self, message: str = "Job title not found.", status_code: int = status.HTTP_404_NOT_FOUND):
        super().__init__(message, status_code)
 