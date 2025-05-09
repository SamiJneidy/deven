from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum, func
from sqlalchemy.orm import relationship
from ..core.database.database import Base
from ..core.enums import UserRole, UserStatus
from .base import AuditMixin

class User(Base, AuditMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=True)
    address = Column(String, nullable=True)
    role = Column(SQLEnum(UserRole), nullable=False)
    status = Column(SQLEnum(UserStatus), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=True)
    last_login = Column(DateTime, nullable=True)
    invalid_login_attempts = Column(Integer, nullable=False, default=0)
    
    company = relationship("app.models.company.Company", back_populates="users")