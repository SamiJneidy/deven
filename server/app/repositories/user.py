from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate, SignUp

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    async def get_user_by_id(self, id: int) -> User | None:
        return self.db.query(User).filter(User.id == id).first()

    async def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    async def signup(self, data: SignUp) -> User:
        db_user = User(**data.model_dump(exclude_unset=True))
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    async def create_user(self, data: UserCreate) -> User:
        db_user = User(**data.model_dump(exclude_unset=True))
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user