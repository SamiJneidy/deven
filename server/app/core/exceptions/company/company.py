from ..base import BaseAppException
from fastapi import status

class CompanyNotFoundError(BaseAppException):
    """Raised when the company is not found."""
    def __init__(self, message: str = "Company not found.", status_code: int = status.HTTP_404_NOT_FOUND):
        super().__init__(message, status_code)