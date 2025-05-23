from math import ceil
from app.repositories import EmployeeRepository, EmployeeEducationRepository, WorkTypeRepository, JobTitleRepository
from app.schemas.hr.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeEducationCreate,
    EmployeeEducationResponse,
    EmployeeEducationUpdate,
)
from app.schemas.common import PaginatedResponse
from app.core.exceptions import (
    EmployeeNotFoundException,
    PersonalEmailAlreadyInUseException,
    WorkEmailAlreadyInUseException,
    EmployeeEducationNotFound
)


class EmployeeService:
    def __init__(self, employee_repository: EmployeeRepository, employee_education_repository: EmployeeEducationRepository):
        self.employee_repository = employee_repository
        self.employee_education_repository = employee_education_repository

    async def get_employee_by_id(self, id: int) -> EmployeeResponse:
        employee = await self.employee_repository.get_employee_by_id(id)
        if not employee:
            raise EmployeeNotFoundException()
        return employee

    async def get_employee_by_personal_email(self, email: str) -> EmployeeResponse:
        employee = await self.employee_repository.get_employee_by_personal_email(email)
        if not employee:
            raise EmployeeNotFoundException()
        return employee

    async def get_employee_by_work_email(self, email: str) -> EmployeeResponse:
        employee = await self.employee_repository.get_employee_by_work_email(email)
        if not employee:
            raise EmployeeNotFoundException()
        return employee

    async def get_employees(
        self, page: int, limit: int
    ) -> PaginatedResponse[EmployeeResponse]:
        skip = (page - 1) * limit
        db_employees, total_rows = await self.employee_repository.get_employees(
            skip, limit
        )
        employees = [
            EmployeeResponse.model_validate(db_employee)
            for db_employee in db_employees
        ]
        pages = ceil(total_rows / limit)
        return PaginatedResponse[EmployeeResponse](
            data=employees,
            total_rows=total_rows,
            total_pages=pages,
            current_page=page,
            limit=limit,
        )

    async def create_employee(self, employee_data: EmployeeCreate) -> EmployeeResponse:
        if await self.employee_repository.get_employee_by_personal_email(
            employee_data.personal_email
        ):
            raise PersonalEmailAlreadyInUseException()
        if await self.employee_repository.get_employee_by_work_email(
            employee_data.work_email
        ):
            raise WorkEmailAlreadyInUseException()
        db_employee = await self.employee_repository.create_employee(
            employee_data.model_dump(exclude={"education"})
        )
        for education in employee_data.education:
            education_dict: dict = education.model_dump()
            education_dict["employee_id"] =  db_employee.id
            await self.employee_education_repository.create_employee_education(education_dict)

        return EmployeeResponse.model_validate(db_employee)

    async def update_employee(self, employee_data: EmployeeUpdate) -> EmployeeResponse:
        if await self.employee_repository.get_employee_by_personal_email(
            employee_data.personal_email
        ):
            raise PersonalEmailAlreadyInUseException()
        if await self.employee_repository.get_employee_by_work_email(
            employee_data.work_email
        ):
            raise WorkEmailAlreadyInUseException()
        db_employee = await self.employee_repository.update_employee(
            employee_data.model_dump()
        )
        return EmployeeResponse.model_validate(db_employee)

    async def delete_employee(self, id: int) -> None:
        employee = await self.employee_repository.get_employee_by_id(id)
        if not employee:
            raise EmployeeNotFoundException()
        await self.employee_repository.delete_employee(id)
