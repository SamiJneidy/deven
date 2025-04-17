from fastapi import APIRouter, status, HTTPException
from ...schemas.common import SignleObjectResponse
from ...schemas.otp import OTPResponse, OTPVerification, OTPVerificationResponse
from ...schemas.user import SignUp, UserResponse
from ...services.user import UserService
from ...services.otp import OTPService
from ...core.dependencies import Annotated, Depends, get_user_service, get_otp_service
from ...core.enums import OTPStatus, OTPUsage

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


@router.post(
    path="/verify-otp", 
    response_model=OTPVerificationResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "The verification has been completed successfully."
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Verification failed",
            "content": {
                "application/json": {
                    "examples": {
                        "InvalidOTPError": {
                            "value": {
                                "code": status.HTTP_401_UNAUTHORIZED,
                                "message": "Invalid OTP"
                            }
                        },
                        "ExpiredOTPError": {
                            "value": {
                                "code": status.HTTP_401_UNAUTHORIZED,
                                "message": "OTP code has expired. Please request a new one."
                            }
                        },
                        "OTPAlreadyUsedError": {
                            "value": {
                                "code": status.HTTP_401_UNAUTHORIZED,
                                "message": "The OTP code has been used before. Please request a new one."
                            }
                        }
                    }
                }
            }
        }
    }
)
async def verify_otp(
    otp_verification_data: OTPVerification,
    otp_service: Annotated[OTPService, Depends(get_otp_service)],
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    """Verify an OTP code. Note that in case the OTP code is used for email verification, the user with this email will be set as 'active'.""" 
    otp_verification_response: OTPVerificationResponse = await otp_service.verify_otp(otp_verification_data)
    otp: OTPResponse = await otp_service.get_otp_by_code(otp_verification_data.code)
    if otp.usage == OTPUsage.EMAIL_VERIFICATION:
        await user_service.verify_user(email=otp.email)
    return otp_verification_response

@router.delete(
    path="/",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_source(
    email: str,
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    """Deletes a user by email. This endpoint is used only during the development."""
    await user_service.delete_user(email)