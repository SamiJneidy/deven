from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime, date
from typing import Annotated
from app.schemas.common import AuditTimeMixin, AuditByMixin, AuditMixin
from app.core.enums import Gender, Country, MartialStatus, EmployeeStatus

class JobTitleBase(BaseModel):

    firstname: str = Field(..., min_length=1, example="Sami")
    lastname: str = Field(..., min_length=1, example="Jneidy")
    gender: Gender = Field(..., example=Gender.MALE)
    date_of_birth: date = Field(..., example="1980-02-17", description="Date of birth following the format: 'yyyy-mm-dd'")
    country: Country = Field(..., example=Country.USA)
    education: str | None = Field(default=None, example="BA in Computer Science")
    martial_status: MartialStatus = Field(..., example=MartialStatus.Married)
    children: int | None = Field(defaule=None, example=2)
    address: str | None = Field(defaule=None, exmple="NY, Brooklyn")
    years_of_experience: int | None = Field(..., example=1)
    # Contact
    work_email: EmailStr = Field(..., example="samihanijneidy@deven.com")
    personal_email: EmailStr = Field(..., example="samihanijneidy@gmail.com")
    phone: str = Field(..., example="+963934989517")
    emergency_phone: str | None = Field(default=None, example="+963934989517")
    emergency_email: EmailStr | None = Field(default=None, example="mehdyasaad@gmail.com")
    # Job info
    job_title_id: int = Field(..., example=1)
    department_id: int = Field(..., example=1)
    shift_id: int = Field(int, example=1)
    work_type_id: int = Field(int, example=1)
    reporting_manager_id: int = Field(..., example=1)
    company_branch_id: int = Field(..., example=1)
    date_of_joining: date = Field(..., example="2025-05-01", description="Date of joining following the format: 'yyyy-mm-dd'")
    in_probation: bool = Field(..., example=True)
    probation_period: int | None = Field(default=None, example=4, description="Probation period in weeks.")
    # System info
    status: EmployeeStatus = Field(..., example=EmployeeStatus.WORKING)


class JobTitleCreate(JobTitleBase):
    pass

class JobTitleUpdate(JobTitleBase):
    pass

class JobTitleResponse(JobTitleBase, AuditMixin):
    id: int
    company_id: int
    model_config = ConfigDict(from_attributes=True)

