from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete, func
from app.models import EmployeeDocument
from app.core.exceptions.database_exceptions import ForeignKeyViolationException

class EmployeeDocumentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_employee_document_by_id(self, id: int) -> EmployeeDocument | None:
        return self.db.query(EmployeeDocument).filter(EmployeeDocument.id == id).first()
    
    async def get_employee_documents(self, skip: int, limit: int, employee_id) -> tuple[list[EmployeeDocument], int]:
        data = self.db.query(EmployeeDocument).filter(EmployeeDocument.employee_id==employee_id).offset(skip).limit(limit).all()
        total_rows = self.db.execute(select(func.count(EmployeeDocument.id)).where(EmployeeDocument.employee_id==employee_id)).scalar()
        return data, total_rows

    async def create_employee_document(self, data: dict) -> EmployeeDocument:
        try:
            db_employee_document = EmployeeDocument(**data)
            self.db.add(db_employee_document)
            self.db.commit()
            self.db.refresh(db_employee_document)
            return db_employee_document
        except IntegrityError as e:
            self.db.rollback()
            raise ForeignKeyViolationException()
        
    async def update_employee_document(self, id: int, data: dict) -> EmployeeDocument:
        try:
            self.db.execute(update(EmployeeDocument).where(EmployeeDocument.id==id).values(**data))
            self.db.commit()
            return await self.get_employee_document_by_id(id)
        except IntegrityError as e:
            self.db.rollback()
            raise ForeignKeyViolationException()
        
    async def delete_employee_document(self, id: int) -> int | None:
        deleted_document_id = self.db.execute(delete(EmployeeDocument).where(EmployeeDocument.id==id).returning(EmployeeDocument.id))
        self.db.commit()
        return deleted_document_id
