from typing import Generic, TypeVar
from pydantic import BaseModel, EmailStr, StringConstraints, ConfigDict, Field


T = TypeVar("T")

class SignleObjectResponse(BaseModel, Generic[T]):
    data: T = Field(..., description="This may be any schema value")
