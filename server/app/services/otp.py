from datetime import datetime, timedelta, timezone
from ..models.otp import OTPStatus, OTPUsage
from ..repositories.otp import OTPRepository
from ..core.exceptions.otp_exceptions import InvalidOTPError, ExpiredOTPError, OTPAlreadyUsedError, SuspiciousOTPActivityError, MultipleOTPsDetectedError
from ..core.config.settings import settings
from ..core.utilities.mail import send_email 
from ..schemas.otp import OTPCreate, OTPVerification, OTPVerificationResponse

class OTPService:
    def __init__(self, otp_repository: OTPRepository):
        self.otp_repository = otp_repository

    async def create_email_verification_otp(self, email: str) -> None:
        """Creates an OTP code for email verification and sends it via email."""
        # Revole all existing email verification codes for this user
        usage: OTPUsage = OTPUsage.EMAIL_VERIFICATION 
        await self.otp_repository.revoke_otps_for_user(email, usage)
        # Generate a new unique OTP code
        while True:   
            code: str = await self.otp_repository.generate_code()
            code_count: int = await self.otp_repository.get_otp_count_by_code(code)
            if code_count == 0:
                break
        
        status: OTPStatus = OTPStatus.PENDING
        # Calculate expiration time for the generated OTP
        expires_at = datetime.now() + timedelta(minutes=settings.EMAIL_VERIFICATION_OTP_EXPIRATION_MINUTES)
        # Insert the generated OTP to the database
        otp_data: OTPCreate = OTPCreate(
            email=email, 
            code=code, 
            usage=usage, 
            status=status, 
            expires_at=expires_at
        )
        db_otp = await self.otp_repository.create_otp(otp_data)
        await self.send_otp_for_email_verification(email, code)

    async def otp_expired(self, code: str) -> bool:
        db_otp = await self.otp_repository.get_otp_by_code(code)
        if db_otp.expires_at < datetime.now():
            return True
        return False

    async def verify_otp(self, otp_verification_data: OTPVerification) -> OTPVerificationResponse:
        db_otp = await self.otp_repository.get_otp_by_code(otp_verification_data.code)
        if db_otp is None:
            raise InvalidOTPError()
        if db_otp.email != otp_verification_data.email:
            raise SuspiciousOTPActivityError()
        if await self.otp_expired(otp_verification_data.code):
            raise ExpiredOTPError()
        if db_otp.status == OTPStatus.EXPIRED or db_otp.status == OTPStatus.VERIFIED:
            raise OTPAlreadyUsedError()
        
        await self.otp_repository.verify_otp(otp_verification_data.code)
        return OTPVerificationResponse(message="Verification completed.")
    
    async def send_otp_for_email_verification(self, email: str, code: str) -> None:
        await send_email(
            to=[email],
            subject="Email verification",
            body=f"Please use this code to verify your account: {code}"
        )   
