from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenPayload(BaseModel):
    email: str
    iat: datetime
    exp: datetime

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