from app.schemas.authentication.authentication import (
    TokenPayload,
    TokenResponse,
    SignUp,
    Login,
    PasswordResetRequest,
    PasswordResetResponse,
    PasswordResetOTPRequest,
    PasswordResetOTPResponse,
)
from app.schemas.authentication.otp import OTPCreate, OTPResponse, OTPVerificationRequest, OTPVerificationResponse