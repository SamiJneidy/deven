from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update, func
from datetime import datetime, timedelta, timezone
import secrets
from ..models.otp import OTP
from ..core.enums import OTPUsage, OTPStatus
from ..core.config.settings import settings
from ..schemas.otp import OTPCreate

class OTPRepository:
    def __init__(self, db: Session):
        self.db = db

    async def generate_code(self, length: int = 6) -> str:
        """Generate an OTP code with a specified length (6 by default)."""
        return "".join(secrets.choice("0123456789") for _ in range(length))

    async def revoke_otps_for_user(self, email: str, usage: OTPUsage) -> None:
        """Revoke all generated OTPs for a specific user."""
        self.db.execute(delete(OTP).where(OTP.email==email, OTP.usage==usage))
        self.db.commit()

    async def get_otp_by_email(self, code: str, usage: OTPUsage) -> OTP | None:
        return self.db.query(OTP).filter(OTP.code==code, OTP.usage==usage).first()

    async def get_otp_by_code(self, code: str) -> OTP | None:
        return self.db.query(OTP).filter(OTP.code==code).first()

    async def get_otp_count_by_user(self, email: str, usage: OTPUsage) -> int:
        """Returns the number of OTPs for a specific user with some usage."""
        return self.db.execute(select(func.count()).select_from(OTP).where(OTP.email==email, OTP.usage==usage)).scalar()

    async def get_otp_count_by_code(self, code: str) -> int:
        """Returns the number of OTPs with this code. Used to maintain uniqueness when genrating new codes."""
        return self.db.execute(select(func.count()).select_from(OTP).where(OTP.code==code)).scalar()
       
    async def create_otp(self, otp_data: OTPCreate) -> OTP:
        """Inserts a new OTP to the database"""
        db_otp = OTP(**otp_data.model_dump())
        self.db.add(db_otp)
        self.db.commit()
        self.db.refresh(db_otp)
        return db_otp

    async def verify_otp(self, code: str) -> None:
        """Sets the status of an OTP code as 'verified'."""
        self.db.execute(update(OTP).where(OTP.code==code).values(status=OTPStatus.VERIFIED))
        self.db.commit()