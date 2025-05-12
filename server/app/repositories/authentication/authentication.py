from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from app.models import User

class AuthenticationRepository:
    def __init__(self, db: Session):
        self.db = db
    
    async def reset_password(self, email: str, hashed_password: str) -> User | None:
        db_user = self.db.query(User).filter(User.email == email).first()
        db_user.password = hashed_password
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

#     async def get_user_by_email(self, email: str) -> User | None:
#         return self.db.query(User).filter(User.email == email).first()

#     async def create_user(self, data: UserCreate) -> User:
#         db_user = User(**data.model_dump(exclude_unset=True))
#         self.db.add(db_user)
#         self.db.commit()
#         self.db.refresh(db_user)
#         return db_user
    
#     async def verify_user(self, email: str) -> None:
#         """Sets the user status to 'active'"""
#         self.db.execute(update(User).where(User.email==email).values(status=UserStatus.ACTIVE))
#         self.db.commit()

#     async def delete_user(self, email: str) -> None:
#         """Deletes a user from the database. Note that this is NOT a soft delete, this will delete the user permanently from the database."""
#         self.db.execute(delete(User).where(User.email==email))
#         self.db.commit()
