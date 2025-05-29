from datetime import datetime, timedelta, timezone
from app.core.enums import OTPStatus, OTPUsage
from app.repositories import OTPRepository
from app.core.exceptions.service_exceptions import InvalidOTPException, ExpiredOTPException, OTPAlreadyUsedException, OTPNotFoundException
from app.core.config.settings import settings
from app.core.utilities.mail import send_email 
from app.schemas import OTPCreate, OTPResponse, OTPVerificationRequest, OTPVerificationResponse

class OTPService:
    def __init__(self, otp_repository: OTPRepository):
        self.otp_repository = otp_repository

    async def get_otp_by_code(self, code: str) -> OTPResponse:
        db_otp = await self.otp_repository.get_otp_by_code(code)
        if db_otp is None:
            raise OTPNotFoundException()
        return OTPResponse.model_validate(db_otp)

    async def get_otp_by_email(self, email: str, usage: OTPUsage) -> OTPResponse:
        db_otp = await self.otp_repository.get_otp_by_email(email, usage)
        if db_otp is None:
            raise OTPNotFoundException()
        return OTPResponse.model_validate(db_otp)

    async def create_email_verification_otp(self, email: str) -> OTPResponse:
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
        db_otp = await self.otp_repository.create_otp(otp_data.model_dump())
        await self.send_otp_for_email_verification(email, code)
        return OTPResponse.model_validate(db_otp)

    async def create_password_reset_otp(self, email: str) -> OTPResponse:
        """Creates an OTP code for password reset and sends it via email."""
        # Revole all existing password reset codes for this user
        usage: OTPUsage = OTPUsage.PASSWORD_RESET 
        await self.otp_repository.revoke_otps_for_user(email, usage)
        # Generate a new unique OTP code
        while True:   
            code: str = await self.otp_repository.generate_code()
            code_count: int = await self.otp_repository.get_otp_count_by_code(code)
            if code_count == 0:
                break
        
        status: OTPStatus = OTPStatus.PENDING
        # Calculate expiration time for the generated OTP
        expires_at = datetime.now() + timedelta(minutes=settings.PASSWORD_RESET_OTP_EXPIRATION_MINUTES)
        # Insert the generated OTP to the database
        otp_data: OTPCreate = OTPCreate(
            email=email, 
            code=code, 
            usage=usage, 
            status=status, 
            expires_at=expires_at
        )
        db_otp = await self.otp_repository.create_otp(otp_data.model_dump())
        await self.send_otp_for_password_reset(email, code)
        return OTPResponse.model_validate(db_otp)
    

    async def otp_expired(self, code: str) -> bool:
        db_otp = await self.otp_repository.get_otp_by_code(code)
        if db_otp.expires_at < datetime.now():
            return True
        return False

    async def verify_otp(self, otp_verification_data: OTPVerificationRequest) -> OTPVerificationResponse:
        db_otp = await self.otp_repository.get_otp_by_code(otp_verification_data.code)
        if db_otp is None:
            raise InvalidOTPException()
        if await self.otp_expired(otp_verification_data.code):
            raise ExpiredOTPException()
        if db_otp.status == OTPStatus.EXPIRED or db_otp.status == OTPStatus.VERIFIED:
            raise OTPAlreadyUsedException()
        
        await self.otp_repository.verify_otp(otp_verification_data.code)
        return OTPVerificationResponse(email=db_otp.email, message="Verification completed.")
    
    async def send_otp_for_email_verification(self, email: str, code: str) -> None:
        await send_email(
            to=[email],
            subject="Email verification",
            body=f"Please use this code to verify your account: {code}"
        )   

    async def send_otp_for_password_reset(self, email: str, code: str) -> None:
        await send_email(
            to=[email],
            subject="Password Reset",
            body=f"Please use this code to reset your password: {code}"
        )   