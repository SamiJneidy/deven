from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated
from redis.asyncio import Redis
from app.core.context import current_user
from app.core.config.settings import settings
from app.core.database.database import get_db
from app.repositories import UserRepository, AuthenticationRepository
from app.services import OTPService, AuthenticationService, UserService, CompanyService
from app.schemas import UserResponse
from app.core.dependencies.user import get_user_service, get_user_repository
from app.core.dependencies.company import get_company_service
from app.core.dependencies.authentication.otp import get_otp_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/authentication/swaggerlogin")

# Redis
async def get_redis():
    redis = Redis.from_url(settings.REDIS_URL)
    try:
        yield redis
    finally:
        await redis.close()

def get_authentication_repository(db: Annotated[Session, Depends(get_db)]) -> AuthenticationRepository:
    """Returns authentication repository dependency."""
    return AuthenticationRepository(db)

def get_authentication_service(
    authentication_repo: Annotated[AuthenticationRepository, Depends(get_authentication_repository)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    otp_service: Annotated[OTPService, Depends(get_otp_service)],
    company_service: Annotated[CompanyService, Depends(get_company_service)],
) -> AuthenticationService:
    """Returns authentication service dependency."""
    return AuthenticationService(authentication_repo, user_repo, user_service, otp_service, company_service)

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], 
    auth_service: Annotated[AuthenticationService, Depends(get_authentication_service)]
) -> UserResponse:
    """Returns the current user from the token."""
    user = await auth_service.get_user_from_token(token)
    current_user.set(user)
    return user

