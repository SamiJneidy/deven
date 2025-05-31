from math import ceil
from fastapi import UploadFile
from app.core.utilities.file_uploader import upload_file, delete_file
from app.repositories import EmployeeDocumentRepository, EmployeeEducationRepository, EmployeeRepository, WorkTypeRepository, JobTitleRepository
from app.schemas.common import PaginatedResponse
from app.schemas.hr.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    ProfilePicture
)
from app.core.exceptions.service_exceptions import (
    EmployeeNotFoundException,
    PersonalEmailAlreadyInUseException,
    WorkEmailAlreadyInUseException,
)


class EmployeeService:
    def __init__(
        self, 
        employee_repository: EmployeeRepository,
        education_repository: EmployeeEducationRepository,
        document_repository: EmployeeDocumentRepository
    ):
        self.employee_repository = employee_repository
        self.education_repository = education_repository
        self.document_repository = document_repository


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
        db_employee = await self.employee_repository.create_employee(
            employee_data.model_dump(exclude={"education"})
        )
        for education in employee_data.education:
            education_dict: dict = education.model_dump()
            education_dict["employee_id"] =  db_employee.id
            await self.education_repository.create_employee_education(education_dict)
        return EmployeeResponse.model_validate(db_employee)

    async def update_employee(self, id: int, employee_data: EmployeeUpdate) -> EmployeeResponse:
        db_employee = await self.employee_repository.update_employee(
            id, employee_data.model_dump(exclude_unset=True)
        )
        return EmployeeResponse.model_validate(db_employee)

    async def delete_employee(self, id: int) -> None:
        employee = await self.employee_repository.get_employee_by_id(id)
        if not employee:
            raise EmployeeNotFoundException()
        await self.employee_repository.delete_employee(id)

    async def upload_profile_picture(self, id: int, image: UploadFile) -> ProfilePicture:
        employee = await self.employee_repository.get_employee_by_id(id)
        if not employee:
            raise EmployeeNotFoundException()
        image_url, public_id = upload_file(image, "profile-pictures")
        await self.employee_repository.upload_profile_picture(id, image_url, public_id)
        return ProfilePicture(profile_picture_url=image_url, profile_picture_public_id=public_id)

    async def remove_profile_picture(self, id: int) -> None:
        employee = await self.employee_repository.get_employee_by_id(id)
        if not employee:
            raise EmployeeNotFoundException()
        delete_file(employee.profile_picture_public_id)
        await self.employee_repository.remove_profile_picture(id)
        