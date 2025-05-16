from pydantic import BaseModel, ConfigDict, Field
from app.schemas.common import AuditMixin

class ShiftBase(BaseModel):
    name: str = Field(..., min_length=1, example="Fulltime")
    

class ShiftCreate(ShiftBase):
    pass

class ShiftUpdate(ShiftBase):
    pass

class ShiftResponse(ShiftBase, AuditMixin):
    id: int
    company_id: int
    model_config = ConfigDict(from_attributes=True)

