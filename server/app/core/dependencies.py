from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated
from redis.asyncio import Redis
from .config.settings import settings
from .database.database import get_db
from ..repositories import UserRepository, OTPRepository, AuthRepository 
from ..services import UserService, OTPService, AuthService
from ..schemas import UserResponse

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


# Auth
def get_auth_repository(db: Annotated[Session, Depends(get_db)]) -> AuthRepository:
    """Returns auth repository dependency."""
    return AuthRepository(db)

def get_auth_service(
    auth_repo: Annotated[AuthRepository, Depends(get_auth_repository)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    otp_service: Annotated[OTPService, Depends(get_otp_service)],
) -> AuthService:
    """Returns auth service dependency."""
    return AuthService(auth_repo, user_repo, user_service, otp_service)

# JWT
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], 
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> UserResponse:
    return await auth_service.get_user_from_token(token)

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
