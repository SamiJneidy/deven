from fastapi import status
from app.core.exceptions.service_exceptions.base import BaseAppException

class EmployeeDocumentNotFoundException(BaseAppException):
    """Raised when the education is not found."""
    def __init__(self, detail: str = "Document not found.", status_code: int = status.HTTP_404_NOT_FOUND):
        super().__init__(detail, status_code)

class EmployeeDocumentUploadFailedException(BaseAppException):
    """Raised when the document was not uploaded successfully."""
    def __init__(self, detail: str = "Could not upload the document. Try again later", status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(detail, status_code)
