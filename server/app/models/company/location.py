from sqlalchemy import Column, String, Integer, Text, Enum as SQLEnum, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from ...core.database import Base
from ..base import BaseModel

class Location(Base, BaseModel):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=True)
    
    employees = relationship("Employee", back_populates="location")
    company = relationship("Company", back_populates="locations")
