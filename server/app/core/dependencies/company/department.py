from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
from app.core.database.database import get_db
from app.repositories import DepartmentRepository
from app.services import DepartmentService

def get_department_repository(db: Annotated[Session, Depends(get_db)]) -> DepartmentRepository:
    """Returns department repository dependency"""
    return DepartmentRepository(db)

def get_department_service(department_repo: Annotated[DepartmentRepository, Depends(get_department_repository)]) -> DepartmentService:
    """Returns department service dependency"""
    return DepartmentService(department_repo)
