from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
from app.core.database.database import get_db
from app.core.dependencies.hr.employee_education import get_employee_education_repository
from app.repositories import EmployeeRepository, EmployeeEducationRepository
from app.services import EmployeeService

def get_employee_repository(db: Annotated[Session, Depends(get_db)]) -> EmployeeRepository:
    """Returns employee education repository dependency"""
    return EmployeeRepository(db)

def get_employee_service(
    employee_repo: Annotated[EmployeeRepository, Depends(get_employee_repository)],
    employee_education_repo: Annotated[EmployeeEducationRepository, Depends(get_employee_education_repository)]
) -> EmployeeService:
    """Returns employee education service dependency"""
    return EmployeeService(employee_repo, employee_education_repo)
