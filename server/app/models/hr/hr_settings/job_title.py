from sqlalchemy import Column, Integer, String, Date, Time, DateTime, ForeignKey, Boolean, Enum as SQLEnum, func
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.common import BaseModel

class JobTitle(Base, BaseModel):
    __tablename__ = "job_titles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    employees = relationship("Employee", back_populates="job_title")
    company = relationship("Company", back_populates="job_titles")
