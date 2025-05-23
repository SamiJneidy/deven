from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated
from redis.asyncio import Redis
from app.core.context import current_user
from app.core.config.settings import settings
from app.core.database.database import get_db
from app.repositories import UserRepository, OTPRepository, AuthenticationRepository, CompanyRepository
from app.services import UserService, OTPService, AuthenticationService, CompanyService
from app.schemas import UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/authentication/swaggerlogin")

# Redis
async def get_redis():
    redis = Redis.from_url(settings.REDIS_URL)
    try:
        yield redis
    finally:
        await redis.close()

# OTP
def get_otp_repository(db: Annotated[Session, Depends(get_db)]) -> OTPRepository:
    """Returns otp repository dependency"""
    return OTPRepository(db)

def get_otp_service(otp_repo: Annotated[OTPRepository, Depends(get_otp_repository)]) -> OTPService:
    """Returns otp service dependency"""
    return OTPService(otp_repo)


# User
def get_user_repository(db: Annotated[Session, Depends(get_db)]) -> UserRepository:
    """Returns user repository dependency."""
    return UserRepository(db)

def get_user_service(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    otp_service: Annotated[OTPService, Depends(get_otp_service)]    
) -> UserService:
    """Returns user service dependency."""
    return UserService(user_repo, otp_service)

# Company
def get_company_repository(db: Annotated[Session, Depends(get_db)]) -> CompanyRepository:
    return CompanyRepository(db)

def get_company_service(
    company_repo: Annotated[CompanyRepository, Depends(get_company_repository)]    
) -> CompanyService:
    """Returns company service dependency."""
    return CompanyService(company_repo)


# Auth
def get_auth_repository(db: Annotated[Session, Depends(get_db)]) -> AuthenticationRepository:
    """Returns auth repository dependency."""
    return AuthenticationRepository(db)

def get_auth_service(
    auth_repo: Annotated[AuthenticationRepository, Depends(get_auth_repository)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    otp_service: Annotated[OTPService, Depends(get_otp_service)],
    company_service: Annotated[CompanyService, Depends(get_company_service)],
) -> AuthenticationService:
    """Returns auth service dependency."""
    return AuthenticationService(auth_repo, user_repo, user_service, otp_service, company_service)

# JWT
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], 
    auth_service: Annotated[AuthenticationService, Depends(get_auth_service)]
) -> UserResponse:
    """Returns the current user from the token."""
    user = await auth_service.get_user_from_token(token)
    current_user.set(user)
    return user

