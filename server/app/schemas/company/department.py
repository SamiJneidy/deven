from pydantic import BaseModel, ConfigDict, Field
from app.schemas.common import AuditMixin

class DepartmentBase(BaseModel):
    name: str = Field(..., min_length=1, example="IT")

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(DepartmentBase):
    pass

class DepartmentResponse(DepartmentBase, AuditMixin):
    id: int
    company_id: int
    model_config = ConfigDict(from_attributes=True)

class DepartmentNestedResponse(DepartmentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)