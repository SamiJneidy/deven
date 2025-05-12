from .authentication.authentication import (
    InvalidCredentialsError,
    UserNotActiveError,
    PasswordResetNotAllowedError,
    PasswordsDontMatchError,
    EmailAlreadyInUseError,
    InvalidTokenError,
)

from .user.users import (
    UserNotFoundError,
)

from .authentication.otp import (
    InvalidOTPError,
    ExpiredOTPError,
    OTPAlreadyUsedError,
    MultipleOTPsDetectedError,
    SuspiciousOTPActivityError,
    OTPNotFoundError
)

from .company.company import CompanyNotFoundError

from .hr import (
    EmployeeNotFound,
    PersonalEmailAlreadyInUseError,
    WorkEmailAlreadyInUseError,
)