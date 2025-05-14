from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from app.models import Department

class DepartmentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_department_by_id(self, id: int) -> Department | None:
        return self.db.query(Department).filter(Department.id == id).first()

    async def get_departments(self, skip: int, limit: int) -> list[Department]:
        return self.db.query(Department).offset(skip).limit(limit).all()

    async def create_department(self, data: dict) -> Department:
        db_department = Department(**data)
        self.db.add(db_department)
        self.db.commit()
        self.db.refresh(db_department)
        return db_department

    async def update_department(self, id: int, data: dict) -> Department:
        self.db.execute(update(Department).where(Department.id==id).values(**data))
        self.db.commit()
        return await self.get_department_by_id(id)
    
    async def delete_department(self, id: int) -> None:
        self.db.execute(delete(Department).where(Department.id==id))
        self.db.commit()
