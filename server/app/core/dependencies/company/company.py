from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
from ...database.database import get_db
from ....repositories import CompanyRepository
from ....services import CompanyService

# Company
def get_company_repository(db: Annotated[Session, Depends(get_db)]) -> CompanyRepository:
    return CompanyRepository(db)

def get_company_service(
    company_repo: Annotated[CompanyRepository, Depends(get_company_repository)]    
) -> CompanyService:
    """Returns company service dependency."""
    return CompanyService(company_repo)
