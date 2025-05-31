from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete, func
from sqlalchemy.exc import IntegrityError
from app.models import Employee
from app.core.exceptions.database_exceptions import (
    ForeignKeyViolationException,
    UniqueConstraintViolationException,
    IntegrityException,
)
from app.core.utilities import raise_classified_integrity_error


class EmployeeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    # Employee data
    async def get_employee_by_id(self, id: int) -> Employee | None:
        return self.db.query(Employee).filter(Employee.id == id).first()

    async def get_employee_by_personal_email(self, email: str) -> Employee | None:
        return self.db.query(Employee).filter(Employee.personal_email == email).first()

    async def get_employee_by_work_email(self, email: str) -> Employee | None:
        return self.db.query(Employee).filter(Employee.work_email == email).first()

    async def get_employees(self, skip: int, limit: int) -> tuple[list[Employee], int]:
        data = self.db.query(Employee).offset(skip).limit(limit).all()
        total_rows = self.db.execute(select(func.count(Employee.id))).scalar()
        return data, total_rows

    async def create_employee(self, data: dict) -> Employee:
        try:
            db_employee = Employee(**data)
            self.db.add(db_employee)
            self.db.commit()
            self.db.refresh(db_employee)
            return db_employee
        except IntegrityError as e:
            raise_classified_integrity_error(e)

    async def update_employee(self, id: int, data: dict) -> Employee:
        try:
            self.db.execute(update(Employee).where(Employee.id == id).values(**data))
            self.db.commit()
            return await self.get_employee_by_id(id)
        except IntegrityError as e:
            raise_classified_integrity_error(e)

    async def delete_employee(self, id: int) -> None:
        self.db.execute(delete(Employee).where(Employee.id == id))
        self.db.commit()

    async def upload_profile_picture(
        self, id: int, image_url: str, public_id: str
    ) -> tuple[str, str]:
        db_employee = self.db.execute(
            update(Employee)
            .where(Employee.id == id)
            .values(profile_picture_url=image_url, profile_picture_public_id=public_id)
            .returning(Employee)
        )
        self.db.commit()
        return image_url, public_id

    async def remove_profile_picture(self, id: int) -> Employee | None:
        db_employee = self.db.execute(
            update(Employee)
            .where(Employee.id == id)
            .values(profile_picture_url="", profile_picture_public_id="")
            .returning(Employee)
        )
        self.db.commit()
        return db_employee
