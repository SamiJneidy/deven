from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
from app.core.database.database import get_db
from app.repositories import JobTitleRepository
from app.services import JobTitleService

def get_job_title_repository(db: Annotated[Session, Depends(get_db)]) -> JobTitleRepository:
    """Returns job title repository dependency"""
    return JobTitleRepository(db)

def get_job_title_service(job_title_repo: Annotated[JobTitleRepository, Depends(get_job_title_repository)]) -> JobTitleService:
    """Returns job title service dependency"""
    return JobTitleService(job_title_repo)
