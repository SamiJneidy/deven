from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str
    iat: datetime | None = None
    exp: datetime | None = None

class SignUp(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    firstname: str = Field(..., example="Sami", min_length=1)
    lastname: str = Field(..., example="Jneidy", min_length=1)
    password: str = Field(..., example="abcABC123", min_length=8, description="The password must be a minimum of 8 characters in length, containing both uppercase and lowercase English letters and at least one numeric digit.")

class Login(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., example="abcABC123")


class PasswordResetRequest(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., example="abcABC123", min_length=8, description="The password must be a minimum of 8 characters in length, containing both uppercase and lowercase English letters and at least one numeric digit.")
    confirm_password: str = Field(..., example="abcABC123", min_length=8, description="The password must be a minimum of 8 characters in length, containing both uppercase and lowercase English letters and at least one numeric digit.")

class PasswordResetResponse(BaseModel):
    pass

class PasswordResetOTPRequest(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")

class PasswordResetOTPResponse(BaseModel):
    message: str = Field(..., example="The OTP code has been sent to your email. Check your inbox or spam folder.")