from ..repositories.user import UserRepository
from ..schemas.user import UserCreate, UserResponse, SignUp
from ..core.security.passwords import hash_password
from ..core.exceptions.base_exceptions import ResourceAlreadyInUseError

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def signup(self, user_data: SignUp) -> UserResponse:
        if await self.user_repository.get_user_by_email(user_data.email):
            raise ResourceAlreadyInUseError("Email")
        
        user_data.password = hash_password(user_data.password)

        db_user = await self.user_repository.create_user(user_data)
        return UserResponse.model_validate(db_user)

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        if await self.user_repository.get_user_by_email(user_data.email):
            raise ResourceAlreadyInUseError("Email")
        
        user_data.password = hash_password(user_data.password)

        db_user = await self.user_repository.create_user(user_data)
        return UserResponse.model_validate(db_user)