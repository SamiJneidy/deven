from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from ....models import Employee, WorkType, JobTitle
from ....core.enums import BusinessType

class EmployeeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_employee_by_id(self, id: int) -> Employee | None:
        return self.db.query(Employee).filter(Employee.id == id).first()

    async def get_employee_by_personal_email(self, email: str) -> WorkType | None:
        return self.db.query(Employee).filter(Employee.personal_email == email).first()

    async def get_employee_by_work_email(self, email: str) -> WorkType | None:
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

class WorkTypeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_work_type_by_id(self, id: int) -> WorkType | None:
        return self.db.query(WorkType).filter(WorkType.id == id).first()

    async def create_work_type(self, data: dict) -> WorkType:
        db_work_type = WorkType(**data)
        self.db.add(db_work_type)
        self.db.commit()
        self.db.refresh(db_work_type)
        return db_work_type

    async def update_work_type(self, id: int, data: dict) -> WorkType:
        self.db.execute(update(WorkType).where(WorkType.id==id).values(**data))
        self.db.commit()
        return await self.get_work_type_by_id(id)
    
    async def delete_work_type(self, id: int) -> None:
        self.db.execute(delete(WorkType).where(WorkType.id==id))
        self.db.commit()

class JobTitleRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_job_title_by_id(self, id: int) -> JobTitle | None:
        return self.db.query(JobTitle).filter(JobTitle.id == id).first()

    async def create_job_title(self, data: dict) -> JobTitle:
        db_job_title = JobTitle(**data)
        self.db.add(db_job_title)
        self.db.commit()
        self.db.refresh(db_job_title)
        return db_job_title

    async def update_work_type(self, id: int, data: dict) -> JobTitle:
        self.db.execute(update(JobTitle).where(JobTitle.id==id).values(**data))
        self.db.commit()
        return await self.get_job_title_by_id(id)
    
    async def delete_job_title(self, id: int) -> None:
        self.db.execute(delete(JobTitle).where(JobTitle.id==id))
        self.db.commit()
