from pydantic import BaseModel, ConfigDict, Field
from app.schemas.common import AuditMixin

class JobTitleBase(BaseModel):
    name: str = Field(..., min_length=1, example="Backend developer")

class JobTitleCreate(JobTitleBase):
    pass

class JobTitleUpdate(JobTitleBase):
    pass

class JobTitleResponse(JobTitleBase, AuditMixin):
    id: int
    company_id: int
    model_config = ConfigDict(from_attributes=True)

