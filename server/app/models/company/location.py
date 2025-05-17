from sqlalchemy import Column, String, Integer, Text, Enum as SQLEnum, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.common import BaseModel, AddressMixin

class Location(Base, BaseModel, AddressMixin):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    
    employees = relationship("Employee", back_populates="location")
    company = relationship("Company", back_populates="locations")
