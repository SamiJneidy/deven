from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import date
from app.schemas.common import AddressMixin, AuditMixin
from app.core.enums import Gender, MartialStatus, EmployeeStatus

class EmployeeEducationBase(BaseModel):
    field_of_study: str = Field(..., example="Computer Science")
    degree: str = Field(..., example="BA")
    institution: str = Field(default=None, example="MIT")
    start_date: date = Field(default=None, example="2020-04-02")
    end_date: date = Field(default=None, example="2025-05-01")
    grade: str = Field(default=None, exmpale="88%")
    status: str = Field(default=None, example="Completed")

class EmployeeEducationOnboarding(EmployeeEducationBase):
    """Used when onboarding a new employee within the EmplyeeCreate schema"""
    pass

class EmployeeEducationCreate(EmployeeEducationBase):
    """Used when creating a new education for an existing employee"""
    employee_id: int

class EmployeeEducationUpdate(EmployeeEducationBase):
    pass 

class EmployeeEducationResponse(EmployeeEducationBase, AuditMixin):
    id: int
    company_id: int
    employee_id: int
    model_config = ConfigDict(from_attributes=True)


class EmployeeBase(BaseModel, AddressMixin):
    firstname: str = Field(..., min_length=1, example="Sami")
    lastname: str = Field(..., min_length=1, example="Jneidy")
    gender: Gender = Field(..., example=Gender.MALE)
    date_of_birth: date = Field(..., example="1980-02-17", description="Date of birth following the format: 'yyyy-mm-dd'")
    martial_status: MartialStatus = Field(..., example=MartialStatus.Married)
    children: int | None = Field(defaule=None, example=2)
    years_of_experience: int | None = Field(default=None, example=1)
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
    reporting_manager_id: int | None = Field(default=None, example=1)
    location_id: int = Field(..., example=1)
    date_of_joining: date = Field(..., example="2025-05-01", description="Date of joining following the format: 'yyyy-mm-dd'")
    in_probation: bool = Field(..., example=True)
    probation_period: int | None = Field(default=None, example=4, description="Probation period in weeks.")
    # System info
    status: EmployeeStatus = Field(..., example=EmployeeStatus.WORKING)


class EmployeeCreate(EmployeeBase):
    education: list[EmployeeEducationCreate]
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase, AuditMixin):
    id: int
    company_id: int
    education: list[EmployeeEducationResponse]
    model_config = ConfigDict(from_attributes=True)
