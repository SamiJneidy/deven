from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete, func
from app.models import Shift

class ShiftRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_shift_by_id(self, id: int) -> Shift | None:
        return self.db.query(Shift).filter(Shift.id == id).first()

    async def get_shifts(self, skip: int, limit: int) -> tuple[list[Shift], int]:
        data = self.db.query(Shift).offset(skip).limit(limit).all()
        total_rows = self.db.execute(select(func.count(Shift.id))).scalar()
        return data, total_rows

    async def create_shift(self, data: dict) -> Shift:
        db_shift = Shift(**data)
        self.db.add(db_shift)
        self.db.commit()
        self.db.refresh(db_shift)
        return db_shift

    async def update_shift(self, id: int, data: dict) -> Shift:
        self.db.execute(update(Shift).where(Shift.id==id).values(**data))
        self.db.commit()
        return await self.get_shift_by_id(id)
    
    async def delete_shift(self, id: int) -> None:
        self.db.execute(delete(Shift).where(Shift.id==id))
        self.db.commit()
