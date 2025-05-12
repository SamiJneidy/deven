from sqlalchemy import Column, Integer, String, Date, Time, DateTime, ForeignKey, Boolean, Enum as SQLEnum, func
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import BaseModel

class WorkType(Base, BaseModel):
    __tablename__ = "work_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    
    employees = relationship("Employee", back_populates="work_type")
    company = relationship("Company", back_populates="work_types")
