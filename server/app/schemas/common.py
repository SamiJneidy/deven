from typing import Generic, TypeVar
from pydantic import BaseModel, EmailStr, StringConstraints, ConfigDict, Field
from datetime import datetime

T = TypeVar("T")

class SignleObjectResponse(BaseModel, Generic[T]):
    """Used when returning a single object get response"""
    data: T = Field(..., description="This may be any schema value")
    
class PaginationResponse(BaseModel, Generic[T]):
    """Used when returning a paginated response"""
    data: list[T]
    total_rows: int | None = None
    total_pages: int | None = None
    current_page: int | None = None
    limit: int | None = None

class ObjectListResponse(BaseModel, Generic[T]):
    """Used when returning an array of objects from a get response"""
    data: list[T] = Field(..., description="This may be any schema value")
    

class AuditByMixin:
    """Adds created_by and updated_by columns to a schema."""
    created_by: int
    updated_by: int | None

class AuditTimeMixin:
    """Adds created_at and updated_at columns to a schema."""
    created_at: datetime
    updated_at: datetime | None

class AuditMixin(AuditByMixin, AuditTimeMixin):
    """Adds created_at, created_by, updated_at and updated_by to a schema."""
    pass
