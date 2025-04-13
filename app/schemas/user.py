from pydantic import BaseModel, EmailStr, StringConstraints, ConfigDict
from datetime import datetime
from typing import Annotated

NonEmptyStr = Annotated[str, StringConstraints(min_length=1)]

class UserBase(BaseModel):
    email: EmailStr
    firstname: NonEmptyStr
    lastname: NonEmptyStr
    phone: str | None = None
    address: str | None = None
    role_id: int | None = None
    status_id: int | None = None

class UserCreate(UserBase):
    password: NonEmptyStr

class UserUpdate(UserBase):
    pass

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    pass