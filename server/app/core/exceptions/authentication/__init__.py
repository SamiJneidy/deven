from app.core.exceptions.authentication.authentication import (
    InvalidCredentialsError,
    UserNotActiveError,
    PasswordResetNotAllowedError,
    PasswordsDontMatchError,
    EmailAlreadyInUseError,
    InvalidTokenError,
)

from app.core.exceptions.authentication.otp import (
    InvalidOTPError,
    ExpiredOTPError,
    OTPAlreadyUsedError,
    MultipleOTPsDetectedError,
    SuspiciousOTPActivityError,
    OTPNotFoundError
)