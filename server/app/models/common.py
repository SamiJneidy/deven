from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from app.core.context import current_user, current_company

class AuditByMixin:
    """Adds created_by and updated_by columns to a model."""
    created_by = Column(Integer, ForeignKey('users.id'), default=lambda: current_user.get().id if current_user.get() else None, nullable=True)
    updated_by = Column(Integer, ForeignKey('users.id'), onupdate=lambda: current_user.get().id if current_user.get() else None, nullable=True)

class AuditTimeMixin:
    """Adds created_at and updated_at columns to a model."""
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

class CompanyMixin:
    """Adds company info to a model."""
    company_id = Column(Integer, ForeignKey('companies.id'), default=lambda: current_user.get().company_id, nullable=False)

class AddressMixin:
    """Adds address fields to a model."""
    country = Column(String, nullable=False)
    state = Column(String, nullable=False)
    city = Column(String, nullable=False)
    postal_code = Column(String, nullable=True)
    address_line1 = Column(String, nullable=True)
    address_line2 = Column(String, nullable=True)

class AuditMixin(AuditByMixin, AuditTimeMixin):
    """Adds created_at, created_by, updated_at and updated_by to a model."""
    pass

class BaseModel(AuditMixin, CompanyMixin):
    """The base model. Contains comapny and audit info."""
    pass