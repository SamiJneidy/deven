from sqlalchemy import Column, Integer, String, Date, Time, DateTime, ForeignKey, Boolean, Enum as SQLEnum, func
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.common import BaseModel

class EmployeeDocument(Base, BaseModel):
    __tablename__ = "employee_documents"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    public_id = Column(String, nullable=False)

    employee = relationship("Employee", foreign_keys=[employee_id], back_populates="documents")
