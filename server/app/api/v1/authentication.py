from fastapi import APIRouter, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from redis.asyncio import Redis
from ...schemas import (
    SignleObjectResponse,
    OTPResponse, 
    OTPVerificationRequest, 
    OTPVerificationResponse, 
    UserResponse,
    SignUp,
    Login,
    TokenResponse,
    PasswordResetRequest,
    PasswordResetOTPRequest,
    PasswordResetOTPResponse,
)
from ...services import UserService, OTPService, AuthService
from ...core.dependencies import (
    Annotated, 
    Session,
    Depends, 
    get_auth_service, 
    get_user_service, 
    get_otp_service,
    get_redis,
    oauth2_scheme
)
from ...core.enums import OTPUsage
from ...core.config.settings import settings

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
                    "examples": {
                        "EmailAlreadyInUse":{
                            "value": {
                                "code": status.HTTP_409_CONFLICT, 
                                "message": "Email already in use."
                            }
                        },
                    }
                }
            }
        }
    }
)
async def signup(
    user_data: SignUp,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    """Sign up a new user""" 
    data = await auth_service.signup(user_data)
    return SignleObjectResponse[UserResponse](data=data)

@router.post(
    path="/login",
    response_model=TokenResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "Logged in successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The user was not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "UserNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "User not found."
                            }
                        },
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "The user is not active.",
            "content": {
                "application/json": {
                    "examples": {
                        "UserNotActive": {
                            "value": {
                                "code": status.HTTP_400_BAD_REQUEST,
                                "message": "User is not active."
                            }
                        },
                    }
                }
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials.",
            "content": {
                "application/json": {
                    "examples": {
                        "InvalidCredentials": {
                            "value": {
                                "code": status.HTTP_401_UNAUTHORIZED,
                                "message": "Invalid credentials."
                            }
                        },
                    }
                }
            }
        }
    }
)
async def login(
    response: Response,
    login_data: Login,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    access_token, refresh_token = await auth_service.create_tokens_for_login(login_data)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=settings.REFRESH_TOKEN_EXPIRATION_DAYS * 24 * 60 * 60,
        path="/authentication/refresh"
    
    )
    return TokenResponse(access_token=access_token)

@router.post(
    path="/logout",
    responses={
        status.HTTP_200_OK: {
            "description": "Logged out successfully.",
            "content": {
                "application/json": {
                    "examples": {
                        "LoggedOutSuccessfully": {
                            "value": {
                                "code": status.HTTP_200_OK,
                                "message": "Logged out successfully."
                            }
                        },
                    }
                }
            }
        }
    }
)
async def logout(token: str = Depends(oauth2_scheme), redis: Redis = Depends(get_redis)):
    await redis.setex(f"blacklist:{token}", 600, "revoked")
    return {"message": "Logged out successfully"}


@router.post(
    path="/request-password-reset-otp", 
    response_model=PasswordResetOTPResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "The OTP code has been sent successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The user who requested the password reset was not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "UserNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "User not found."
                            }
                        },  
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "The user who requested password reset is not active.",
            "content": {
                "application/json": {
                    "examples": {
                        "UserNotActive": {
                            "value": {
                                "code": status.HTTP_400_BAD_REQUEST,
                                "message": "User is not active."
                            }
                        },
                    }
                }
            }
        }
    }
)
async def request_password_reset_otp(
    password_reset_otp_request: PasswordResetOTPRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],

):
    """Create a password reset OTP and send it to the user via email. Note that in case the user account was not active then the code will not be sent.""" 
    return await auth_service.request_password_reset_otp(password_reset_otp_request)


@router.post(
    path="/reset-password", 
    response_model=UserResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "The password has been reset successfully."
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "The password could not be reset due to OTP error or security reason.",
            "content": {
                "application/json": {
                    "examples": {
                        "PasswordResetNotAllowed": {
                            "value": {
                                "code": status.HTTP_401_UNAUTHORIZED,
                                "message": "Password reset not allowed. Request a new OTP code and try again."
                            }
                        },
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "The new password must match the confirmation password.",
            "content": {
                "application/json": {
                    "examples": {
                        "PasswordsDontMatch": {
                            "value": {
                                "code": status.HTTP_400_BAD_REQUEST,
                                "message": "Passwords don't match."
                            }
                        },
                    }
                }
            }
        }
    }
)
async def reset_password(
    password_reset_request: PasswordResetRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    """Resets the password of the user. Note that the user has verify the OTP code in order to reset his password.""" 
    return await auth_service.reset_password(password_reset_request)


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
                                "message": "Invalid OTP."
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
    otp_verification_data: OTPVerificationRequest,
    otp_service: Annotated[OTPService, Depends(get_otp_service)],
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    """Verify an OTP code for email verification, password reset, ...etc. Note that in case the usage of the code is email verification, the user with this email will be set as 'active'.""" 
    otp_verification_response: OTPVerificationResponse = await otp_service.verify_otp(otp_verification_data)
    otp: OTPResponse = await otp_service.get_otp_by_code(otp_verification_data.code)
    if otp.usage == OTPUsage.EMAIL_VERIFICATION:
        await user_service.verify_user(email=otp.email)
    return otp_verification_response


@router.delete(
    path="/",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
    email: str,
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    """Deletes a user by email. This endpoint is used only during the development."""
    await user_service.delete_user(email)


@router.post(
    path="/swaggerlogin", 
    responses={
        status.HTTP_200_OK: {
            "description": "Logged in successfully",
        },
    },
)
async def swaggerlogin(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    response: Response,
    login_credentials: OAuth2PasswordRequestForm = Depends(), 
):
    """This is for SwaggerUI authentication for testing purposes only. Don't use this endpoint if you want to login as a frontend, use the login endpoint instead."""
    login_data = Login(email=login_credentials.username, password=login_credentials.password)
    access_token, refresh_token = await auth_service.create_tokens_for_login(login_data)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=settings.REFRESH_TOKEN_EXPIRATION_DAYS * 24 * 60 * 60,
        path="/authentication/refresh"
    
    )
    return {"access_token": access_token, "token_type": "bearer"}