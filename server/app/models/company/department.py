from sqlalchemy import Column, String, Integer, Text, Enum as SQLEnum, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import BaseModel

class Department(Base, BaseModel):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    # manager_id = Column(Integer, ForeignKey('employees.id'), nullable=True)
    
    # manager = relationship("Employee", foreign_keys=[manager_id], remote_side="Employee.id", back_populates="managed_departments")
    employees = relationship("Employee", foreign_keys="[Employee.department_id]", back_populates="department")
    company = relationship("Company", back_populates="departments")
