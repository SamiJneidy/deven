from app.repositories import DepartmentRepository
from app.schemas.company import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from app.core.exceptions.company import DepartmentNotFoundException

class DepartmentService:
    def __init__(self, department_repository: DepartmentRepository) -> None:
        self.department_repository = department_repository

    async def get_department_by_id(self, id: int) -> DepartmentResponse:
        db_department = await self.department_repository.get_department_by_id(id)
        if not db_department:
            raise DepartmentNotFoundException()
        return DepartmentResponse.model_validate(db_department)

    async def get_departments(self, skip: int, limit: int) -> list[DepartmentResponse]:
        db_departments = await self.department_repository.get_departments(skip, limit)
        departments = [DepartmentResponse.model_validate(db_department) for db_department in db_departments]
        return departments

    async def create_department(self, department_data: DepartmentCreate) -> DepartmentResponse:
        db_department = await self.department_repository.create_department(department_data.model_dump())
        return DepartmentResponse.model_validate(db_department)

    async def update_department(self, id: int, department_data: DepartmentUpdate) -> DepartmentResponse:
        db_department = await self.department_repository.get_department_by_id(id)
        if not db_department:
            raise DepartmentNotFoundException()
        db_department = await self.department_repository.update_department(id, department_data.model_dump())
        return DepartmentResponse.model_validate(db_department)

    async def delete_department(self, id: int) -> None:
        db_department = await self.department_repository.get_department_by_id(id)
        if not db_department:
            raise DepartmentNotFoundException()
        await self.department_repository.delete_department(id)
