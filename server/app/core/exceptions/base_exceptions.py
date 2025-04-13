class BaseAppException(Exception):
    """Base exception for service-layer errors."""
    
    def __init__(self, detail: str = None):
        self.detail = detail or "An internal server error occurred."
        super().__init__(self.detail)

class ResourceAlreadyInUseError(BaseAppException):
    """Raised when trying to register a resource that's already in use."""
    def __init__(self, resource_name: str = "Resource", detail: str = None):
        detail = detail or f"{resource_name} already in use"
        super().__init__(detail)

class ResourceNotFoundError(BaseAppException):
    """Raised when trying to access a resource that doesn't exist."""
    def __init__(self, resource_name: str = "Resource", detail: str = None):
        detail = detail or f"{resource_name} not found"
        super().__init__(detail)

