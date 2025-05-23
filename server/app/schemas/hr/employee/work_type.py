from pydantic import BaseModel, ConfigDict, Field
from app.schemas.common import AuditMixin

class WorkTypeBase(BaseModel):
    name: str = Field(..., min_length=1, example="Fulltime")
    
class WorkTypeCreate(WorkTypeBase):
    pass

class WorkTypeUpdate(WorkTypeBase):
    pass

class WorkTypeResponse(WorkTypeBase, AuditMixin):
    id: int
    company_id: int
    model_config = ConfigDict(from_attributes=True)

class WorkTypeNestedResponse(WorkTypeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
