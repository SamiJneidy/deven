from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
from app.core.database.database import get_db
from app.repositories import ShiftRepository
from app.services import ShiftService

def get_shift_repository(db: Annotated[Session, Depends(get_db)]) -> ShiftRepository:
    """Returns shift repository dependency"""
    return ShiftRepository(db)

def get_shift_service(shift_repo: Annotated[ShiftRepository, Depends(get_shift_repository)]) -> ShiftService:
    """Returns shift service dependency"""
    return ShiftService(shift_repo)
