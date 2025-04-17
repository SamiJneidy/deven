from .otp import OTPService
from .user import UserService
from ..repositories.auth import AuthRepository
from ..core.security.passwords import hash_password
from ..schemas.user import UserCreate, UserResponse, SignUp
from ..schemas.otp import OTPResponse
from ..schemas.auth import PasswordResetRequest, PasswordResetResponse, PasswordResetOTPRequest, PasswordResetOTPResponse
from ..core.exceptions.base_exceptions import ResourceAlreadyInUseError
from ..core.exceptions.auth_exceptions import UserNotActiveError, PasswordResetNotAllowedError, PasswordsDontMatchError
from ..core.exceptions.otp_exceptions import OTPNotFoundError
from ..core.enums import UserRole, UserStatus, OTPStatus, OTPUsage

class AuthService:
    def __init__(self, auth_repository: AuthRepository, user_service: UserService, otp_service: OTPService):
        self.auth_repository = auth_repository
        self.user_service = user_service
        self.otp_service = otp_service

    async def request_password_reset_otp(self, password_reset_otp_request: PasswordResetOTPRequest) -> PasswordResetOTPResponse:
        user: UserResponse = await self.user_service.get_user_by_email(password_reset_otp_request.email)
        if user.status != UserStatus.ACTIVE:
            raise  UserNotActiveError()
        await self.otp_service.create_password_reset_otp(password_reset_otp_request.email)
        return PasswordResetOTPResponse(message="The OTP code has been sent to your email. Check your inbox or spam folder.")
    
    async def reset_password(self, password_reset_request: PasswordResetRequest) -> UserResponse:
        try:
            otp: OTPResponse = await self.otp_service.get_otp_by_email(password_reset_request.email, OTPUsage.PASSWORD_RESET)
            if otp.status != OTPStatus.VERIFIED or password_reset_request.email != otp.email or await self.otp_service.otp_expired(otp.code):
                raise PasswordResetNotAllowedError()
            if password_reset_request.password != password_reset_request.confirm_password:
                raise PasswordsDontMatchError()
            hashed_password = hash_password(password_reset_request.password)
            db_user = await self.auth_repository.reset_password(password_reset_request.email, hashed_password)
            return UserResponse.model_validate(db_user)
        except OTPNotFoundError:
            raise PasswordResetNotAllowedError()
        