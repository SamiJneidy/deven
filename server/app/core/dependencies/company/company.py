from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
from app.core.database.database import get_db
from app.repositories import CompanyRepository
from app.services import CompanyService

# Company
def get_company_repository(db: Annotated[Session, Depends(get_db)]) -> CompanyRepository:
    return CompanyRepository(db)

def get_company_service(
    company_repo: Annotated[CompanyRepository, Depends(get_company_repository)]    
) -> CompanyService:
    """Returns company service dependency."""
    return CompanyService(company_repo)
