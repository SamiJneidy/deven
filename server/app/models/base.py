from sqlalchemy import Column, DateTime, Integer, ForeignKey, func
from ..core.database.database import Base
from ..core.context import current_user

class AuditByMixin:
    """Adds created_by and updated_by columns to a model."""
    created_by = Column(Integer, ForeignKey('users.id'), default=lambda: current_user.get().id)
    updated_by = Column(Integer, ForeignKey('users.id'), onupdate=lambda: current_user.get().id, nullable=True)

class AuditTimeMixin:
    """Adds created_at and updated_at columns to a model."""
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

class AuditMixin(AuditByMixin, AuditTimeMixin):
    """Adds created_at, created_by, updated_at and updated_by to a model."""
    pass
