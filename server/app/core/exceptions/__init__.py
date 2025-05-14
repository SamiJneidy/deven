from app.core.exceptions.authentication.authentication import (
    InvalidCredentialsException,
    UserNotActiveException,
    PasswordResetNotAllowedException,
    PasswordsDontMatchException,
    EmailAlreadyInUseException,
    InvalidTokenException,
)

from app.core.exceptions.user.users import (
    UserNotFoundException,
)

from app.core.exceptions.authentication.otp import (
    InvalidOTPException,
    ExpiredOTPException,
    OTPAlreadyUsedException,
    MultipleOTPsDetectedException,
    SuspiciousOTPActivityException,
    OTPNotFoundException
)

from app.core.exceptions.company.company import CompanyNotFoundException

from app.core.exceptions.hr import (
    EmployeeNotFoundException,
    PersonalEmailAlreadyInUseException,
    WorkEmailAlreadyInUseException,
)