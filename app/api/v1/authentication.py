from fastapi import APIRouter
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService 
from app.core.dependencies import Annotated, Depends, get_user_service

router = APIRouter(
    prefix="/authentication", 
    tags=["Authentication"],
)

@router.post(
    path="/signup", 
    response_model=UserResponse,
)
async def signup(
    user_data: UserCreate,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    """Sign up a new user"""
    return await user_service.create_user(user_data)