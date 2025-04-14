from fastapi import APIRouter, status
from app.schemas.user import SignUp, UserResponse
from app.services.user import UserService 
from app.core.dependencies import Annotated, Depends, get_user_service

router = APIRouter(
    prefix="/authentication", 
    tags=["Authentication"],
)

@router.post(
    path="/signup", 
    response_model=UserResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "The user has signed up successfully."
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Some fields violates the defined schemas for the request body."
        },
        status.HTTP_409_CONFLICT: {
            "description": "The email has been registered before.",
            "content": {
                "application/json": {
                    "example": {
                        "code": status.HTTP_409_CONFLICT, 
                        "message": "Email already in use."
                    }
                }
            }
        }
    }
)
async def signup(
    user_data: SignUp,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    """Sign up a new user"""
    return await user_service.signup(user_data)