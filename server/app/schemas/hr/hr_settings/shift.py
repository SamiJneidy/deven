from pydantic import BaseModel, ConfigDict, Field, field_serializer
from datetime import time
from app.schemas.common import AuditMixin

class ShiftBase(BaseModel):
    name: str = Field(..., min_length=1, example="Regular shift")
    start_time: time = Field(..., example="09:00")
    end_time: time = Field(..., example="05:00")

    @field_serializer("start_time", "end_time")
    def serialize_time(self, value: time, _info):
        return value.strftime("%H:%M")
    

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
