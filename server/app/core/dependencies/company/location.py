from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
from app.core.database.database import get_db
from app.repositories import LocationRepository
from app.services import LocationService

def get_location_repository(db: Annotated[Session, Depends(get_db)]) -> LocationRepository:
    """Returns location repository dependency"""
    return LocationRepository(db)

def get_location_service(location_repo: Annotated[LocationRepository, Depends(get_location_repository)]) -> LocationService:
    """Returns location service dependency"""
    return LocationService(location_repo)
