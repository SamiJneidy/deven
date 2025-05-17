from pydantic import BaseModel, ConfigDict, Field
from app.schemas.common import AuditMixin, AddressMixin

class LocationBase(BaseModel, AddressMixin):
    name: str = Field(..., min_length=1, example="Head quarters")

class LocationCreate(LocationBase):
    pass

class LocationUpdate(LocationBase):
    pass

class LocationResponse(LocationBase, AuditMixin):
    id: int
    company_id: int
    model_config = ConfigDict(from_attributes=True)

