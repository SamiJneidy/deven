from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from app.core.config.settings import settings
from app.core.database.database import get_db
from app.repositories.user import UserRepository
from app.services.user import UserService

# User
def get_user_repository(db: Annotated[Session, Depends(get_db)]) -> UserRepository:
    """Returns user repository dependency"""
    return UserRepository(db)

def get_user_service(user_repo: Annotated[UserRepository, Depends(get_user_repository)]) -> UserService:
    """Returns user service dependency"""
    return UserService(user_repo)



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
