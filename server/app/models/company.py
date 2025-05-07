from sqlalchemy import Column, String, Integer, Text, Enum as SQLEnum, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from ..core.database.database import Base
from ..core.enums import BusinessType
from .base import AuditTimeMixin, AuditMixin

class Company(Base, AuditTimeMixin):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    country = Column(String, nullable=True)
    website = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    number_of_employees = Column(Integer, nullable=True)
    business_type = Column(SQLEnum(BusinessType), nullable=True)

    users = relationship("User", back_populates="company")
    employees = relationship("Employee", back_populates="company")
    job_titles = relationship("JobTitle", back_populates="company")
    departments = relationship("Department", back_populates="company")
    shifts = relationship("Shift", back_populates="company")
    work_types = relationship("WorkType", back_populates="company")
    locations = relationship("CompanyLocation", back_populates="company")

class CompanyLocation(Base, AuditMixin):
    __tablename__ = "company_locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=True)
    description = Column(String, nullable=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    
    employees = relationship("Employee", back_populates="location")
    company = relationship("Company", foreign_keys=[company_id], back_populates="locations")