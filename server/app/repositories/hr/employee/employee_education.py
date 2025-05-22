from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete, func
from app.models import EmployeeEducation

class EmployeeEducationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_employee_education_by_id(self, id: int) -> EmployeeEducation | None:
        return self.db.query(EmployeeEducation).filter(EmployeeEducation.id == id).first()
    
    async def get_employee_educations(self, skip: int, limit: int, employee_id) -> tuple[list[EmployeeEducation], int]:
        data = self.db.query(EmployeeEducation).filter(EmployeeEducation.employee_id==employee_id).offset(skip).limit(limit).all()
        total_rows = self.db.execute(select(func.count(EmployeeEducation.id)).where(EmployeeEducation.employee_id==employee_id)).scalar()
        return data, total_rows

    async def create_employee_education(self, data: dict) -> EmployeeEducation:
        db_employee_education = EmployeeEducation(**data)
        self.db.add(db_employee_education)
        self.db.commit()
        self.db.refresh(db_employee_education)
        return db_employee_education

    async def update_employee_education(self, id: int, data: dict) -> EmployeeEducation:
        self.db.execute(update(EmployeeEducation).where(EmployeeEducation.id==id).values(**data))
        self.db.commit()
        return await self.get_employee_education_by_id(id)
    
    async def delete_employee_education(self, id: int) -> None:
        self.db.execute(delete(EmployeeEducation).where(EmployeeEducation.id==id))
        self.db.commit()
