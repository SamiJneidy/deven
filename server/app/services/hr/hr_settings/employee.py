from math import ceil
from app.core.utilities.file_uploader import upload_file
from app.repositories import EmployeeRepository, WorkTypeRepository, JobTitleRepository
from app.schemas.common import PaginatedResponse
from app.schemas.hr.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeDocumentCreate,
    EmployeeDocumentResponse,
    EmployeeDocumentUpdate,
    EmployeeDocumentCreate,
    EmployeeEducationCreate,
    EmployeeEducationUpdate,
    EmployeeEducationResponse,
)
from app.core.exceptions import (
    EmployeeEducationNotFoundException,
    EmployeeNotFoundException,
    PersonalEmailAlreadyInUseException,
    WorkEmailAlreadyInUseException,
    EmployeeDocumentNotFoundException,
    EmployeeDocumentUploadFailedException,
)


class EmployeeService:
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository

    # Employee data
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
            await self.employee_repository.create_employee_education(education_dict)

        return EmployeeResponse.model_validate(db_employee)

    async def update_employee(self, id: int, employee_data: EmployeeUpdate) -> EmployeeResponse:
        if await self.employee_repository.get_employee_by_personal_email(
            employee_data.personal_email
        ):
            raise PersonalEmailAlreadyInUseException()
        if await self.employee_repository.get_employee_by_work_email(
            employee_data.work_email
        ):
            raise WorkEmailAlreadyInUseException()
        db_employee = await self.employee_repository.update_employee(
            id, employee_data.model_dump(exclude_unset=True)
        )
        return EmployeeResponse.model_validate(db_employee)

    async def delete_employee(self, id: int) -> None:
        employee = await self.employee_repository.get_employee_by_id(id)
        if not employee:
            raise EmployeeNotFoundException()
        await self.employee_repository.delete_employee(id)

    async def upload_profile_picture(self, id: int, image_url: str) -> None:
        employee = await self.employee_repository.get_employee_by_id(id)
        if not employee:
            raise EmployeeNotFoundException()
        await self.employee_repository.upload_profile_picture(id, image_url)
        
    # Employee document
    async def get_employee_document_by_id(self, employee_id: int, document_id: int) -> EmployeeDocumentResponse:
        # Check if employee exists
        db_employee = await self.employee_repository.get_employee_by_id(employee_id)
        if not db_employee:
            raise EmployeeNotFoundException()
        
        db_employee_document = (
            await self.employee_repository.get_employee_document_by_id(document_id)
        )
        if not db_employee_document:
            raise EmployeeDocumentNotFoundException()
        return EmployeeDocumentResponse.model_validate(db_employee_document)

    async def get_employee_documents(
        self, page: int, limit: int, employee_id: int
    ) -> PaginatedResponse[EmployeeDocumentResponse]:
        # Check if employee exists
        db_employee = await self.employee_repository.get_employee_by_id(employee_id)
        if not db_employee:
            raise EmployeeNotFoundException()
        
        skip = (page - 1) * limit
        db_employee_documents, total_rows = (
            await self.employee_repository.get_employee_documents(
                skip, limit, employee_id
            )
        )
        employee_documents = [
            EmployeeDocumentResponse.model_validate(db_document)
            for db_document in db_employee_documents
        ]
        pages = ceil(total_rows / limit)
        return PaginatedResponse[EmployeeDocumentResponse](
            data=employee_documents,
            total_rows=total_rows,
            total_pages=pages,
            current_page=page,
            limit=limit,
        )

    async def create_employee_document(
        self, employee_id: int, employee_document_data: EmployeeDocumentCreate
    ) -> EmployeeDocumentResponse:
        # Check if employee exists
        db_employee = await self.employee_repository.get_employee_by_id(employee_id)
        if not db_employee:
            raise EmployeeNotFoundException()
        
        try:
            document_url, public_id = upload_file(employee_document_data.file, "documents")
            data = employee_document_data.model_dump()
            data.pop("file")
            data.update({"url": document_url, "public_id": public_id})
            db_employee_document = (
                await self.employee_repository.create_employee_document(data)
            )
            return EmployeeDocumentResponse.model_validate(db_employee_document)
        except Exception as e:
            raise EmployeeDocumentUploadFailedException()
        
    async def update_employee_document(
        self, employee_id: int, document_id: int, employee_document_data: EmployeeDocumentUpdate
    ) -> EmployeeDocumentResponse:
        # Check if employee exists
        db_employee = await self.employee_repository.get_employee_by_id(employee_id)
        if not db_employee:
            raise EmployeeNotFoundException()
        
        db_employee_document = (
            await self.employee_repository.get_employee_document_by_id(document_id)
        )
        if not db_employee_document:
            raise EmployeeDocumentNotFoundException()
        try:
            document_url, public_id = upload_file(employee_document_data.file, "documents")
            data = employee_document_data.model_dump()
            data.pop("file")
            data.update({"url": document_url, "public_id": public_id})
            db_employee_document = (
                await self.employee_repository.update_employee_document(document_id, data)
            )
            return EmployeeDocumentResponse.model_validate(db_employee_document)
        except Exception as e:
            raise EmployeeDocumentUploadFailedException()

    async def delete_employee_document(self, employee_id: int, document_id: int) -> None:
        # Check if employee exists
        db_employee = await self.employee_repository.get_employee_by_id(employee_id)
        if not db_employee:
            raise EmployeeNotFoundException()
                
        db_employee_document = (
            await self.employee_repository.get_employee_document_by_id(document_id)
        )
        if not db_employee_document:
            raise EmployeeDocumentNotFoundException()
        await self.employee_repository.delete_employee_document(document_id)

    # Education
    async def get_employee_education_by_id(self, employee_id: int, education_id: int) -> EmployeeEducationResponse:
        db_employee_education = (
            await self.employee_repository.get_employee_education_by_id(id)
        )
        if not db_employee_education:
            raise EmployeeEducationNotFoundException()
        return EmployeeEducationResponse.model_validate(db_employee_education)

    async def get_employee_educations(
        self, page: int, limit: int, employee_id: int
    ) -> PaginatedResponse[EmployeeEducationResponse]:
        skip = (page - 1) * limit
        db_employee_educations, total_rows = (
            await self.employee_repository.get_employee_educations(
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
        self, 
        employee_id: int, 
        employee_education_data: EmployeeEducationCreate
    ) -> EmployeeEducationResponse:
        db_employee_education = (
            await self.employee_repository.create_employee_education(
                employee_education_data.model_dump()
            )
        )
        return EmployeeEducationResponse.model_validate(db_employee_education)

    async def update_employee_education(
        self, 
        employee_id: int, 
        education_id: int, 
        employee_education_data: EmployeeEducationUpdate
    ) -> EmployeeEducationResponse:
        db_employee_education = (
            await self.employee_repository.get_employee_education_by_id(id)
        )
        if not db_employee_education:
            raise EmployeeEducationNotFoundException()
        db_employee_education = (
            await self.employee_repository.update_employee_education(
                id, employee_education_data.model_dump()
            )
        )
        return EmployeeEducationResponse.model_validate(db_employee_education)

    async def delete_employee_education(self, id: int) -> None:
        db_employee_education = (
            await self.employee_repository.get_employee_education_by_id(id)
        )
        if not db_employee_education:
            raise EmployeeEducationNotFoundException()
        await self.employee_repository.delete_employee_education(id)
