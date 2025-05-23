from pydantic import BaseModel, ConfigDict, Field
from datetime import time
from app.schemas.common import AuditMixin

class ShiftBase(BaseModel):
    name: str = Field(..., min_length=1, example="Regular shift")
    start_time: time = Field(..., example="09:00")
    end_time: time = Field(..., example="05:00")
    

class ShiftCreate(ShiftBase):
    pass

class ShiftUpdate(ShiftBase):
    pass

class ShiftResponse(ShiftBase, AuditMixin):
    id: int
    company_id: int
    model_config = ConfigDict(from_attributes=True)

class ShiftNestedResponse(ShiftBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
