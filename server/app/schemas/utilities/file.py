from pydantic import BaseModel, ConfigDict, Field
from app.schemas.common import AuditMixin

class FileBase(BaseModel):
    name: str = Field(..., min_length=1)
    url: str = Field(..., min_length=1)
    public_id: str = Field(..., min_length=1)
    usage: str = Field(default=None, min_length=1)

class FileCreate(FileBase):
    pass

class FileResponse(FileBase, AuditMixin):
    id: int
    company_id: int
    model_config = ConfigDict(from_attributes=True)

