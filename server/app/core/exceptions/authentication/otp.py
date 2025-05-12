from fastapi import status
from ..base import BaseAppException, ResourceNotFoundError

class InvalidOTPError(BaseAppException):
    """Raised when the OTP code is invalid."""
    def __init__(self, message: str = "Invalid OTP.", status_code: int = status.HTTP_401_UNAUTHORIZED):
        super().__init__(message, status_code)

class ExpiredOTPError(BaseAppException):
    """Raised when the OTP code is expired."""
    def __init__(self, message: str = "OTP code has expired. Please request a new one.", status_code: int = status.HTTP_401_UNAUTHORIZED):
        super().__init__(message, status_code)

class OTPAlreadyUsedError(BaseAppException):
    """Raised when the OTP has already been used and cannot be reused."""
    def __init__(self, message: str = "The OTP code has been used before. Please request a new one.", status_code: int = status.HTTP_401_UNAUTHORIZED):
        super().__init__(message, status_code)

class MultipleOTPsDetectedError(BaseAppException):
    """Raised when multiple OTP codes are found for a single user."""
    def __init__(self, message: str = "OTP verification error. Please request a new code.", status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(message, status_code)

class SuspiciousOTPActivityError(BaseAppException):
    """Raised when a security issue is detected with the OTP process."""
    def __init__(self, message: str = "Unusual activiy has been detected. Operation aborted for security issues.", status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(message, status_code)

class OTPNotFoundError(BaseAppException):
    """Raised when the OTP is not found."""
    def __init__(self, message: str = "OTP not found.", status_code: int = status.HTTP_404_NOT_FOUND):
        super().__init__(message, status_code)
