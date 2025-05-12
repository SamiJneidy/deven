from ..authentication import OTPService
from ...repositories import OTPRepository, UserRepository
from ...schemas import UserCreate, UserResponse
from ...core.security.passwords import hash_password
from ...core.exceptions import EmailAlreadyInUseError, UserNotFoundError
from ...core.enums import UserRole, UserStatus, OTPStatus, OTPUsage

class UserService:
    def __init__(self, user_repository: UserRepository, otp_service: OTPService):
        self.user_repository = user_repository
        self.otp_service = otp_service

    async def get_user_by_email(self, email: str) -> UserResponse:
        user = await self.user_repository.get_user_by_email(email)
        if not user:
            raise UserNotFoundError()
        return user

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        if await self.user_repository.get_user_by_email(user_data.email):
            raise EmailAlreadyInUseError()
        user_data.password = hash_password(user_data.password)
        db_user = await self.user_repository.create_user(user_data.model_dump())
        return UserResponse.model_validate(db_user)

    async def verify_user(self, email: str) -> None:
        await self.user_repository.verify_user(email)

    async def delete_user(self, email: str) -> None:
        await self.user_repository.delete_user(email)