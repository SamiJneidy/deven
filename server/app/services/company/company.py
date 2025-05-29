from app.repositories import CompanyRepository
from app.schemas import CompanyCreate, CompanyUpdate, CompanyResponse
from app.core.exceptions.service_exceptions import CompanyNotFoundException


class CompanyService:
    def __init__(self, company_repository: CompanyRepository):
        self.company_repository = company_repository

    async def get_company_by_id(self, id: int) -> CompanyResponse:
        db_company = await self.company_repository.get_company_by_id(id)
        if not db_company:
            raise CompanyNotFoundException()
        return CompanyResponse.model_validate(db_company)

    async def create_company(self, company_data: CompanyCreate) -> CompanyResponse:
        db_company = await self.company_repository.create_company(company_data.model_dump())
        return CompanyResponse.model_validate(db_company)

    async def create_initial_company(self, company_name: str = "My Company") -> CompanyResponse:
        company_data = CompanyCreate(name=company_name)
        db_company = await self.company_repository.create_company(company_data.model_dump())
        return CompanyResponse.model_validate(db_company)

    async def update_company(self, id: int, company_data: CompanyUpdate) -> CompanyResponse:
        db_company = await self.company_repository.update_company(id, company_data.model_dump())
        if not db_company:
            raise CompanyNotFoundException()
        return CompanyResponse.model_validate(db_company) 

    async def delete_company(self, id: int) -> None:
        await self.company_repository.delete_company(id)
