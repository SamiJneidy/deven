from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
from app.core.database.database import get_db
from app.repositories import EmployeeEducationRepository
from app.services import EmployeeEducationService

def get_employee_education_repository(db: Annotated[Session, Depends(get_db)]) -> EmployeeEducationRepository:
    """Returns employee education repository dependency"""
    return EmployeeEducationRepository(db)

def get_employee_education_service(employee_education_repo: Annotated[EmployeeEducationRepository, Depends(get_employee_education_repository)]) -> EmployeeEducationService:
    """Returns employee education service dependency"""
    return EmployeeEducationService(employee_education_repo)
