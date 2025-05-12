from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
from ...database.database import get_db
from ....repositories import WorkTypeRepository
from ....services import WorkTypeService

def get_work_type_repository(db: Annotated[Session, Depends(get_db)]) -> WorkTypeRepository:
    """Returns work type repository dependency"""
    return WorkTypeRepository(db)

def get_work_type_service(otp_repo: Annotated[WorkTypeRepository, Depends(get_work_type_repository)]) -> WorkTypeService:
    """Returns work type service dependency"""
    return WorkTypeService(otp_repo)
