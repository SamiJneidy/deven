from pydantic import BaseModel, EmailStr, HttpUrl, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID
from ..common import AuditTimeMixin
from ...core.enums import BusinessType

class CompanyBase(BaseModel):
    name: str = Field(..., example="Deven")
    email: EmailStr | None = Field(default=None, example="company@example.com")
    phone_number: str | None = Field(default=None, example="+963934989517")
    address: str | None = Field(default=None, example="St 40, Latakia, Syria")
    city: str | None = Field(default=None, example="Jableh")
    state: str | None = Field(default=None, example="Latakia")
    postal_code: str | None = Field(default=None, example="0000")
    country: str | None = Field(default=None, example="Syria")
    website: str | None = Field(default=None, example="https://www.mycompany.com")
    logo_url: str | None = Field(default=None, example="https://www.mylogo.com")
    number_of_employees: int | None = Field(default=None, example="40")
    business_type: BusinessType | None = Field(default=None, example="Retail")

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    # name: str | None = Field(default=None, example="Deven")
    pass

class CompanyResponse(CompanyBase, AuditTimeMixin):
    id: int

    model_config = ConfigDict(from_attributes=True)
