from pydantic import BaseModel, ConfigDict, Field
from datetime import date
from app.schemas.common import AuditMixin

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
