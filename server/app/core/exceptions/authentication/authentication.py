from fastapi import status
from app.core.exceptions.base import BaseAppException

class UserNotActiveException(BaseAppException):
    """Raised when the user is not active."""
    def __init__(self, message: str = "User is not active.", status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(message, status_code)

class PasswordResetNotAllowedException(BaseAppException):
    """Raised when trying to reset the password without verifying the OTP code or the email is blocked."""
    def __init__(self, message: str = "Password reset not allowed. Request a new OTP code and try again.", status_code: int = status.HTTP_401_UNAUTHORIZED):
        super().__init__(message, status_code)

class PasswordsDontMatchException(BaseAppException):
    """Raised when reseting the password and the provided passwords don't match."""
    def __init__(self, message: str = "Passwords don't match.", status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(message, status_code)

class InvalidCredentialsException(BaseAppException):
    """Raised when trying to login but the credentials are invalid."""
    def __init__(self, message: str = "Invalid credentials.", status_code: int = status.HTTP_401_UNAUTHORIZED):
        super().__init__(message, status_code)

class EmailAlreadyInUseException(BaseAppException):
    """Raised when the email is already in use."""
    def __init__(self, message: str = "Email already in use.", status_code: int = status.HTTP_409_CONFLICT):
        super().__init__(message, status_code)
 

class InvalidTokenException(BaseAppException):
    """Raised the token is invalid or expired."""
    def __init__(self, message: str = "Invalid token.", status_code: int = status.HTTP_401_UNAUTHORIZED):
        super().__init__(message, status_code)