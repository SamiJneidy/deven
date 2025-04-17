from .otp import OTPService
from .user import UserService
from ..schemas.user import UserCreate, UserResponse, SignUp
from ..schemas.otp import OTPResponse
from ..schemas.auth import PasswordResetOTPRequest, PasswordResetOTPResponse
from ..core.security.passwords import hash_password
from ..core.exceptions.base_exceptions import ResourceAlreadyInUseError
from ..core.exceptions.auth_exceptions import UserNotActiveError
from ..core.enums import UserRole, UserStatus, OTPStatus, OTPUsage

class AuthService:
    def __init__(self, user_service: UserService, otp_service: OTPService):
        self.user_service = user_service
        self.otp_service = otp_service

    async def request_password_reset_otp(self, password_reset_otp_request: PasswordResetOTPRequest) -> PasswordResetOTPResponse:
        user: UserResponse = await self.user_service.get_user_by_email(password_reset_otp_request.email)
        if user.status != UserStatus.ACTIVE:
            raise  UserNotActiveError()
        await self.otp_service.create_password_reset_otp(password_reset_otp_request.email)
        return PasswordResetOTPResponse(message="The OTP code has been sent to your email. Check your inbox or spam folder.")