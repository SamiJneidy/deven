from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
from app.core.database.database import get_db
from app.repositories import EmployeeDocumentRepository
from app.services import EmployeeDocumentService

def get_employee_document_repository(db: Annotated[Session, Depends(get_db)]) -> EmployeeDocumentRepository:
    """Returns employee document repository dependency"""
    return EmployeeDocumentRepository(db)

def get_employee_document_service(employee_document_repo: Annotated[EmployeeDocumentRepository, Depends(get_employee_document_repository)]) -> EmployeeDocumentService:
    """Returns employee document service dependency"""
    return EmployeeDocumentService(employee_document_repo)
