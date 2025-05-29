from app.core.exceptions.service_exceptions.authentication.authentication import (
    InvalidCredentialsException,
    UserNotActiveException,
    PasswordResetNotAllowedException,
    PasswordsDontMatchException,
    EmailAlreadyInUseException,
    InvalidTokenException,
)

from app.core.exceptions.service_exceptions.authentication.otp import (
    InvalidOTPException,
    ExpiredOTPException,
    OTPAlreadyUsedException,
    MultipleOTPsDetectedException,
    SuspiciousOTPActivityException,
    OTPNotFoundException
)