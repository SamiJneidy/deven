from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
from app.core.database.database import get_db
from app.repositories import FileRepository

def get_file_repository(db: Annotated[Session, Depends(get_db)]) -> FileRepository:
    """Returns file repository dependency"""
    return FileRepository(db)
