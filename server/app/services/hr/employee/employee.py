from app.repositories import EmployeeRepository, WorkTypeRepository, JobTitleRepository
from app.schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.core.exceptions import EmployeeNotFound, PersonalEmailAlreadyInUseError, WorkEmailAlreadyInUseError

class EmployeeService:
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository

    async def get_employee_by_id(self, id: int) -> EmployeeResponse:
        employee = await self.employee_repository.get_employee_by_id(id)
        if not employee:
            raise EmployeeNotFound()
        return employee

    async def create_employee(self, employee_data: EmployeeCreate) -> EmployeeResponse:
        if await self.employee_repository.get_employee_by_personal_email(employee_data.personal_email):
            raise PersonalEmailAlreadyInUseError()
        if await self.employee_repository.get_employee_by_work_email(employee_data.work_email):
            raise WorkEmailAlreadyInUseError()
        db_employee = await self.employee_repository.create_employee(employee_data.model_dump())
        return EmployeeResponse.model_validate(db_employee)

    async def update_employee(self, employee_data: EmployeeUpdate) -> EmployeeResponse:
        if await self.employee_repository.get_employee_by_personal_email(employee_data.personal_email):
            raise PersonalEmailAlreadyInUseError()
        if await self.employee_repository.get_employee_by_work_email(employee_data.work_email):
            raise WorkEmailAlreadyInUseError()
        db_employee = await self.employee_repository.update_employee(employee_data.model_dump())
        return EmployeeResponse.model_validate(db_employee)

    async def delete_employee(self, id: int) -> None:
        employee = await self.employee_repository.get_employee_by_id(id)
        if not employee:
            raise EmployeeNotFound()
        await self.employee_repository.delete_employee(id)