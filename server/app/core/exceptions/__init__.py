from app.core.exceptions.authentication.authentication import (
    InvalidCredentialsError,
    UserNotActiveError,
    PasswordResetNotAllowedError,
    PasswordsDontMatchError,
    EmailAlreadyInUseError,
    InvalidTokenError,
)

from app.core.exceptions.user.users import (
    UserNotFoundError,
)

from app.core.exceptions.authentication.otp import (
    InvalidOTPError,
    ExpiredOTPError,
    OTPAlreadyUsedError,
    MultipleOTPsDetectedError,
    SuspiciousOTPActivityError,
    OTPNotFoundError
)

from app.core.exceptions.company.company import CompanyNotFoundError

from app.core.exceptions.hr import (
    EmployeeNotFound,
    PersonalEmailAlreadyInUseError,
    WorkEmailAlreadyInUseError,
)