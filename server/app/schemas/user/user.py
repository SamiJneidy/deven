from pydantic import BaseModel, EmailStr, StringConstraints, ConfigDict, Field
from datetime import datetime
from typing import Annotated
from app.core.enums import UserRole, UserStatus

class UserBase(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    firstname: str = Field(..., example="Sami", min_length=1)
    lastname: str = Field(..., example="Jneidy", min_length=1)
    phone: str | None = Field(default=None, example="+963934989517")
    address: str | None = Field(default=None, example="St 40, Latakia, Syria")
    role: UserRole | None = Field(default=None, example=UserRole.ADMIN)
    status: UserStatus | None = Field(default=None, example=UserStatus.ACTIVE)

class UserCreate(UserBase):
    password: str = Field(..., example="abcABC123", min_length=8, description="The password must be a minimum of 8 characters in length, containing both uppercase and lowercase English letters and at least one numeric digit.")

class UserUpdate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    created_at: datetime
    created_by: int | None
    updated_at: datetime | None
    updated_by: int | None
    company_id: int
    model_config = ConfigDict(from_attributes=True)