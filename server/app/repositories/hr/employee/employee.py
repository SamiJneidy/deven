from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from app.models import Employee

class EmployeeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_employee_by_id(self, id: int) -> Employee | None:
        return self.db.query(Employee).filter(Employee.id == id).first()

    async def get_employee_by_personal_email(self, email: str) -> Employee | None:
        return self.db.query(Employee).filter(Employee.personal_email == email).first()

    async def get_employee_by_work_email(self, email: str) -> Employee | None:
        return self.db.query(Employee).filter(Employee.work_email == email).first()

    async def create_employee(self, data: dict) -> Employee:
        db_employee = Employee(**data)
        self.db.add(db_employee)
        self.db.commit()
        self.db.refresh(db_employee)
        return db_employee

    async def update_employee(self, id: int, data: dict) -> Employee:
        self.db.execute(update(Employee).where(Employee.id==id).values(**data))
        self.db.commit()
        return await self.get_employee_by_id(id)
    
    async def delete_employee(self, id: int) -> None:
        self.db.execute(delete(Employee).where(Employee.id==id))
        self.db.commit()
