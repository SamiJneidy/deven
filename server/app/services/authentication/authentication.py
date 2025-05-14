import jwt
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from app.services.authentication.otp import OTPService
from app.services.user import UserService
from app.services.company import CompanyService
from app.repositories import AuthenticationRepository, UserRepository
from app.core.security.passwords import hash_password, verify_password
from app.core.config.settings import settings
from app.schemas import (
    TokenPayload,
    SignUp, 
    Login,
    UserCreate,
    UserResponse, 
    OTPResponse, 
    PasswordResetRequest, 
    PasswordResetResponse, 
    PasswordResetOTPRequest, 
    PasswordResetOTPResponse,
    CompanyCreate,
    CompanyResponse,
)
from app.core.exceptions import (
    InvalidCredentialsException,
    EmailAlreadyInUseException,
    UserNotActiveException, 
    UserNotFoundException,
    PasswordResetNotAllowedException, 
    PasswordsDontMatchException,
    OTPNotFoundException,
    InvalidTokenException,
)
from app.core.enums import UserRole, UserStatus, OTPStatus, OTPUsage

class AuthenticationService:
    def __init__(self, 
        auth_repository: AuthenticationRepository, 
        user_repository: UserRepository,
        user_service: UserService, 
        otp_service: OTPService,
        company_service: CompanyService,
    ):
        self.auth_repository = auth_repository
        self.user_repository = user_repository
        self.user_service = user_service
        self.otp_service = otp_service
        self.company_service = company_service

    async def signup(self, user_data: SignUp) -> UserResponse:
        """TO BE ADDED"""
        if await self.user_repository.get_user_by_email(user_data.email):
            raise EmailAlreadyInUseException()
        user_data.password = hash_password(user_data.password)
        user_create = UserCreate(**user_data.model_dump())
        user_create.role = UserRole.ADMIN
        user_create.status = UserStatus.PENDING
        user_dict: dict = user_create.model_dump()

        company_data = CompanyCreate(name=f"{user_data.firstname}'s Company")
        company = await self.company_service.create_company(company_data)
        user_dict.update({"company_id": company.id})
        db_user = await self.user_repository.create_user(user_dict)
        x = await self.otp_service.create_email_verification_otp(email=user_data.email)
        print(x.code)
        return UserResponse.model_validate(db_user)

    async def create_tokens_for_login(self, login_data: Login) -> tuple[str, str]:
        """Returns a pair of token after successful login. The pais is (access token, refresh token)."""
        db_user = await self.user_repository.get_user_by_email(login_data.email)
        if not db_user:
            raise UserNotFoundException()
        if db_user.status != UserStatus.ACTIVE:
            raise UserNotActiveException()
        if not verify_password(login_data.password, db_user.password):
            raise InvalidCredentialsException()
        token_payload = TokenPayload(sub=login_data.email)
        access_token = await self.create_access_token(token_payload)
        refresh_token = await self.create_refresh_token(token_payload)
        return (access_token, refresh_token)

    async def request_password_reset_otp(self, password_reset_otp_request: PasswordResetOTPRequest) -> PasswordResetOTPResponse:
        """Request an OTP code for password reset."""
        user: UserResponse = await self.user_service.get_user_by_email(password_reset_otp_request.email)
        if user.status != UserStatus.ACTIVE:
            raise  UserNotActiveException()
        await self.otp_service.create_password_reset_otp(password_reset_otp_request.email)
        return PasswordResetOTPResponse(message="The OTP code has been sent to your email. Check your inbox or spam folder.")
    
    async def reset_password(self, password_reset_request: PasswordResetRequest) -> UserResponse:
        """Reset the password after verifying the OTP code."""
        try:
            otp: OTPResponse = await self.otp_service.get_otp_by_email(password_reset_request.email, OTPUsage.PASSWORD_RESET)
            if otp.status != OTPStatus.VERIFIED or password_reset_request.email != otp.email or await self.otp_service.otp_expired(otp.code):
                raise PasswordResetNotAllowedException()
            if password_reset_request.password != password_reset_request.confirm_password:
                raise PasswordsDontMatchException()
            hashed_password = hash_password(password_reset_request.password)
            db_user = await self.auth_repository.reset_password(password_reset_request.email, hashed_password)
            return UserResponse.model_validate(db_user)
        except OTPNotFoundException:
            raise PasswordResetNotAllowedException()
        
    async def create_access_token(self, token_payload: TokenPayload) -> str:
        """Creates an access token."""
        token_payload.iat = datetime.now(tz=timezone.utc)
        token_payload.exp = datetime.now(tz=timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRATION_MINUTES)
        to_encode = token_payload.model_dump()
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    async def create_refresh_token(self, token_payload: TokenPayload) -> str:
        """Creates a refresh token."""
        token_payload.iat = datetime.now(tz=timezone.utc)
        token_payload.exp = datetime.now(tz=timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRATION_DAYS)
        to_encode = token_payload.model_dump()
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    async def get_user_from_token(self, token: str) -> UserResponse:
        """Extracts user info from a token."""
        try:
            payload_dict: dict = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email = payload_dict.get("sub")
            return await self.user_service.get_user_by_email(email)
        except (jwt.InvalidTokenError, UserNotFoundException):
            raise InvalidTokenException()
        
    