from fastapi import status

class BaseAppException(Exception):
    """Base exception for service-layer errors."""
    def __init__(self, message: str = "An internal server error occurred.", status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code

class ResourceAlreadyInUseException(BaseAppException):
    """Raised when trying to register a resource that's already in use."""
    def __init__(self, resource_name: str = "Resource", message: str = None):
        message = message or f"{resource_name} already in use."
        super().__init__(message, status.HTTP_409_CONFLICT)

class ResourceNotFoundException(BaseAppException):
    """Raised when trying to access a resource that doesn't exist."""
    def __init__(self, resource_name: str = "Resource", message: str = None):
        message = message or f"{resource_name} not found."
        super().__init__(message, status.HTTP_404_NOT_FOUND)
