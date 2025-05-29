from sqlalchemy import Column, Integer, String, Date, Time, DateTime, ForeignKey, Boolean, Enum as SQLEnum, func
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.common import BaseModel

class EmployeeEducation(Base, BaseModel):
    __tablename__ = "employee_education"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    field_of_study = Column(String, nullable=False)
    degree = Column(String, nullable=False)
    institution = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    grade = Column(String, nullable=True)
    status = Column(String, nullable=True)

    employee = relationship("Employee", foreign_keys=[employee_id], back_populates="education")
