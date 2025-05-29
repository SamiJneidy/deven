from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
from app.core.database.database import get_db
from app.core.dependencies.hr.education import get_employee_education_repository
from app.core.dependencies.hr.document import get_employee_document_repository
from app.repositories import EmployeeRepository, EmployeeEducationRepository, EmployeeDocumentRepository
from app.services import EmployeeService

def get_employee_repository(db: Annotated[Session, Depends(get_db)]) -> EmployeeRepository:
    """Returns employee education repository dependency"""
    return EmployeeRepository(db)

def get_employee_service(
    employee_repo: Annotated[EmployeeRepository, Depends(get_employee_repository)],
    employee_education_repo: Annotated[EmployeeEducationRepository, Depends(get_employee_education_repository)],
    employee_document_repo: Annotated[EmployeeDocumentRepository, Depends(get_employee_document_repository)],
) -> EmployeeService:
    """Returns employee education service dependency"""
    return EmployeeService(employee_repo, employee_education_repo, employee_document_repo)
