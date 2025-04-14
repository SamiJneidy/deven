from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from ..core.database.database import Base

class UserRoles(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)    

    users = relationship("User", back_populates="role")

class UserStatus(Base):
    __tablename__ = "user_status"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    users = relationship("User", back_populates="status")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=True)
    address = Column(String, nullable=True)
    role_id = Column(Integer, ForeignKey('user_roles.id'), nullable=True)
    status_id = Column(Integer, ForeignKey('user_status.id'), nullable=True)
    # company_id = Column(Integer, ForeignKey('companies.id'), nullable=True)
    last_login = Column(DateTime, nullable=True)
    invalid_login_attempts = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=func.now())
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())
    updated_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    
    role = relationship("UserRoles", back_populates="users")
    status = relationship("UserStatus", back_populates="users")
    # company = relationship("Company", back_populates="users")