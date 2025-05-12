from sqlalchemy import Column, String, Integer, Text, Enum as SQLEnum, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.enums import BusinessType
from app.models.base import AuditTimeMixin, AuditMixin

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
    # shifts = relationship("Shift", back_populates="company")
    work_types = relationship("WorkType", back_populates="company")
    locations = relationship("Location", back_populates="company")
