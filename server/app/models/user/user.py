from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum, func
from sqlalchemy.orm import relationship
from app.core.database.database import Base
from app.core.enums import UserRole, UserStatus
from app.models.common import BaseModel

class User(Base, BaseModel):
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
    last_login = Column(DateTime, nullable=True)
    invalid_login_attempts = Column(Integer, nullable=False, default=0)
    
    company = relationship("Company", back_populates="users")