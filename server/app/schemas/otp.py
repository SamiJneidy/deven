from pydantic import BaseModel, EmailStr, StringConstraints, ConfigDict, Field
from datetime import datetime
from typing import Annotated
from ..core.enums import OTPStatus, OTPUsage

class OTPBase(BaseModel):
    email: EmailStr 
    code: str
    usage: OTPUsage 
    status: OTPStatus
    expires_at: datetime

class OTPCreate(OTPBase):
    pass

class OTPResponse(OTPBase):
    model_config = ConfigDict(from_attributes=True)

class OTPVerification(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    code: str = Field(..., example="1234656")

class OTPVerificationResponse(BaseModel):
    message: str = Field(..., example="Verification completed.")
