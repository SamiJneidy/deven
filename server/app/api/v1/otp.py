from fastapi import APIRouter, status, HTTPException
from ...schemas.common import SignleObjectResponse
from ...schemas.otp import OTPVerification, OTPVerificationResponse
from ...services.user import OTPService
from ...core.dependencies import Annotated, Depends, get_otp_service

router = APIRouter(
    prefix="/otp", 
    tags=["OTP"],
)

@router.post(
    path="/verify", 
    response_model=OTPVerificationResponse,
    # responses={
    #     status.HTTP_200_OK: {
    #         "description": "The user has signed up successfully."
    #     },
    #     status.HTTP_409_CONFLICT: {
    #         "description": "The email has been registered before.",
    #         "content": {
    #             "application/json": {
    #                 "example": {
    #                     "code": status.HTTP_409_CONFLICT, 
    #                     "message": "Email already in use."
    #                 }
    #             }
    #         }
    #     }
    # }
)
async def verify_otp(
    otp_verification_data: OTPVerification,
    otp_service: Annotated[OTPService, Depends(get_otp_service)],
):
    """Verify an OTP code""" 
    return await otp_service.verify_otp(otp_verification_data)
