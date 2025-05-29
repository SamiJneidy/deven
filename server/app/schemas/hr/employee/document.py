from pydantic import BaseModel, ConfigDict, Field
from fastapi import UploadFile
from app.schemas.common import AuditMixin

class EmployeeDocumentCreate(BaseModel):
    name: str
    file: UploadFile
    employee_id: int

class EmployeeDocumentUpdate(BaseModel):
    name: str
    file: UploadFile

class EmployeeDocumentResponse(BaseModel, AuditMixin):
    id: int
    name: str
    url: str
    public_id: str
    company_id: int
    employee_id: int
    model_config = ConfigDict(from_attributes=True)
