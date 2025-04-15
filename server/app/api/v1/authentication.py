from fastapi import APIRouter, status, HTTPException
from ...schemas.common import SignleObjectResponse
from ...schemas.user import SignUp, UserResponse
from ...services.user import UserService
from ...core.dependencies import Annotated, Depends, get_user_service

router = APIRouter(
    prefix="/authentication", 
    tags=["Authentication"],
)

@router.post(
    path="/signup", 
    response_model=SignleObjectResponse[UserResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The user has signed up successfully."
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
    data = await user_service.signup(user_data)
    return SignleObjectResponse[UserResponse](data=data)
