from fastapi import HTTPException
from .otp import OTPRepository, OTPService
from ..repositories.user import UserRepository
from ..schemas.user import UserCreate, UserResponse, SignUp
from ..core.security.passwords import hash_password
from ..core.exceptions.base_exceptions import ResourceAlreadyInUseError
from ..core.enums import UserRole, UserStatus, OTPStatus, OTPUsage

class UserService:
    def __init__(self, user_repository: UserRepository, otp_service: OTPService):
        self.user_repository = user_repository
        self.otp_service = otp_service

    async def signup(self, user_data: SignUp) -> UserResponse:
        if await self.user_repository.get_user_by_email(user_data.email):
            raise ResourceAlreadyInUseError("Email")
        user_data.password = hash_password(user_data.password)
        user_create = UserCreate(**user_data.model_dump())
        user_create.role = UserRole.ADMIN
        user_create.status = UserStatus.PENDING
        db_user = await self.user_repository.create_user(user_create)
        await self.otp_service.create_email_verification_otp(email=user_data.email)
        return UserResponse.model_validate(db_user)


    async def create_user(self, user_data: UserCreate) -> UserResponse:
        if await self.user_repository.get_user_by_email(user_data.email):
            raise ResourceAlreadyInUseError("Email")
        
        user_data.password = hash_password(user_data.password)

        db_user = await self.user_repository.create_user(user_data)
        return UserResponse.model_validate(db_user)
     