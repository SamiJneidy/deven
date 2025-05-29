from fastapi import status
from app.core.exceptions.service_exceptions.base import BaseAppException

class JobTitleNotFoundException(BaseAppException):
    """Raised when the job title is not found."""
    def __init__(self, detail: str = "Job title not found.", status_code: int = status.HTTP_404_NOT_FOUND):
        super().__init__(detail, status_code)
 