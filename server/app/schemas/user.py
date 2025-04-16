from pydantic import BaseModel, EmailStr, StringConstraints, ConfigDict, Field
from datetime import datetime
from typing import Annotated
from ..core.enums import UserRole, UserStatus

class UserBase(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    firstname: str = Field(..., example="Sami", min_length=1)
    lastname: str = Field(..., example="Jneidy", min_length=1)
    phone: str | None = Field(default=None, example="+963934989517")
    address: str | None = Field(default=None, example="St 40, Latakia, Syria")
    role: UserRole | None = Field(default=None, example=UserRole.ADMIN)
    status: UserStatus | None = Field(default=None, example=UserStatus.ACTIVE)

class SignUp(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    firstname: str = Field(..., example="Sami", min_length=1)
    lastname: str = Field(..., example="Jneidy", min_length=1)
    password: str = Field(..., example="abcABC123", min_length=8, description="The password must be a minimum of 8 characters in length, containing both uppercase and lowercase English letters and at least one numeric digit.")

class UserCreate(UserBase):
    password: str = Field(..., example="abcABC123", min_length=8, description="The password must be a minimum of 8 characters in length, containing both uppercase and lowercase English letters and at least one numeric digit.")

class UserUpdate(UserBase):
    pass

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    pass