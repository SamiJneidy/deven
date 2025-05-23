from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import date
from app.schemas.hr.employee.shift import ShiftNestedResponse
from app.schemas.hr.employee.work_type import WorkTypeNestedResponse
from app.schemas.hr.employee.job_title import JobTitleNestedResponse 
from app.schemas.company.department import DepartmentNestedResponse
from app.schemas.company.location import LocationNestedResponse
from app.schemas.hr.employee.employee_education import EmployeeEducationOnboarding, EmployeeEducationResponse
from app.schemas.common import AddressMixin, AuditMixin
from app.core.enums import Gender, MartialStatus, EmployeeStatus

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
    job_title: JobTitleNestedResponse
    department: DepartmentNestedResponse
    shift: ShiftNestedResponse
    work_type: WorkTypeNestedResponse
    reporting_manager_id: int | None = Field(default=None, example=1)
    location: LocationNestedResponse
    date_of_joining: date = Field(..., example="2025-05-01", description="Date of joining following the format: 'yyyy-mm-dd'")
    in_probation: bool = Field(..., example=True)
    probation_period: int | None = Field(default=None, example=4, description="Probation period in weeks.")
    # System info
    status: EmployeeStatus = Field(..., example=EmployeeStatus.WORKING)


class EmployeeCreate(EmployeeBase):
    education: list[EmployeeEducationOnboarding]
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase, AuditMixin):
    id: int
    company_id: int
    education: list[EmployeeEducationResponse]
    model_config = ConfigDict(from_attributes=True)
