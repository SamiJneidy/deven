from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from .config.settings import settings
from .database.database import get_db
from ..repositories.user import UserRepository
from ..repositories.otp import OTPRepository
from ..services.user import UserService
from ..services.otp import OTPService

# OTP

def get_otp_repository(db: Annotated[Session, Depends(get_db)]) -> OTPRepository:
    """Returns otp repository dependency"""
    return OTPRepository(db)

def get_otp_service(otp_repo: Annotated[OTPRepository, Depends(get_otp_repository)]) -> OTPService:
    """Returns otp service dependency"""
    return OTPService(otp_repo)


# User
def get_user_repository(db: Annotated[Session, Depends(get_db)]) -> UserRepository:
    """Returns user repository dependency"""
    return UserRepository(db)

def get_user_service(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    otp_service: Annotated[OTPService, Depends(get_otp_service)]    
) -> UserService:
    """Returns user service dependency"""
    return UserService(user_repo, otp_service)

# async def get_current_user(
#     db: DBDep,
#     token: str = Depends(security.oauth2_scheme)
# ) -> User:
#     """Validate JWT and return user"""
#     user = security.verify_token(db, token)
#     if not user:
#         raise HTTPException(status.HTTP_401_UNAUTHORIZED)
#     return user

# CurrentUser = Annotated[User, Depends(get_current_user)]
