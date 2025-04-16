from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum as SQLEnum, func
from sqlalchemy.orm import relationship
from ..core.database.database import Base
from ..core.enums import OTPStatus, OTPUsage

class OTP(Base):
    __tablename__ = "otps"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, index=True)
    code = Column(String, unique=True, nullable=False, index=True)
    usage = Column(SQLEnum(OTPUsage), nullable=False)
    status = Column(SQLEnum(OTPStatus), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    