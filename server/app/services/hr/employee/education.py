from math import ceil
from app.repositories import (
    EmployeeEducationRepository,
)
from app.schemas.hr.employee import (
    EmployeeEducationCreate,
    EmployeeEducationResponse,
    EmployeeEducationUpdate,
)
from app.schemas.common import PaginatedResponse
from app.core.exceptions.service_exceptions import EmployeeNotFoundException, EmployeeEducationNotFoundException


class EmployeeEducationService:
    def __init__(self, employee_education_repository: EmployeeEducationRepository):
        self.employee_education_repository = employee_education_repository

    async def get_employee_education_by_id(self, id: int) -> EmployeeEducationResponse:
        db_employee_education = (
            await self.employee_education_repository.get_employee_education_by_id(id)
        )
        if not db_employee_education:
            raise EmployeeEducationNotFoundException()
        return EmployeeEducationResponse.model_validate(db_employee_education)

    async def get_employee_educations(
        self, page: int, limit: int, employee_id: int
    ) -> PaginatedResponse[EmployeeEducationResponse]:
        skip = (page - 1) * limit
        db_employee_educations, total_rows = (
            await self.employee_education_repository.get_employee_educations(
                skip, limit, employee_id
            )
        )
        employee_educations = [
            EmployeeEducationResponse.model_validate(db_education)
            for db_education in db_employee_educations
        ]
        pages = ceil(total_rows / limit)
        return PaginatedResponse[EmployeeEducationResponse](
            data=employee_educations,
            total_rows=total_rows,
            total_pages=pages,
            current_page=page,
            limit=limit,
        )

    async def create_employee_education(
        self, employee_education_data: EmployeeEducationCreate
    ) -> EmployeeEducationResponse:
        db_employee_education = (
            await self.employee_education_repository.create_employee_education(
                employee_education_data.model_dump()
            )
        )
        return EmployeeEducationResponse.model_validate(db_employee_education)

    async def update_employee_education(
        self, id: int, employee_education_data: EmployeeEducationUpdate
    ) -> EmployeeEducationResponse:
        db_employee_education = (
            await self.employee_education_repository.get_employee_education_by_id(id)
        )
        if not db_employee_education:
            raise EmployeeEducationNotFoundException()
        db_employee_education = (
            await self.employee_education_repository.update_employee_education(
                id, employee_education_data.model_dump()
            )
        )
        return EmployeeEducationResponse.model_validate(db_employee_education)

    async def delete_employee_education(self, id: int) -> None:
        db_employee_education = (
            await self.employee_education_repository.get_employee_education_by_id(id)
        )
        if not db_employee_education:
            raise EmployeeEducationNotFoundException()
        await self.employee_education_repository.delete_employee_education(id)
