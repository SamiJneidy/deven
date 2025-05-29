from fastapi import status
from app.core.exceptions.service_exceptions.base import BaseAppException

class CompanyNotFoundException(BaseAppException):
    """Raised when the company is not found."""
    def __init__(self, detail: str = "Company not found.", status_code: int = status.HTTP_404_NOT_FOUND):
        super().__init__(detail, status_code)