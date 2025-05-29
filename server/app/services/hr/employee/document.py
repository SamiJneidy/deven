from math import ceil
from app.repositories import (
    EmployeeDocumentRepository,
)
from app.schemas.hr.employee import (
    EmployeeDocumentCreate,
    EmployeeDocumentResponse,
    EmployeeDocumentUpdate,
)
from app.schemas.common import PaginatedResponse
from app.core.exceptions.service_exceptions import EmployeeDocumentUploadFailedException, EmployeeNotFoundException, EmployeeDocumentNotFoundException
from app.core.utilities.file_uploader import upload_file


class EmployeeDocumentService:
    def __init__(self, document_repository: EmployeeDocumentRepository):
        self.document_repository = document_repository
    
    async def get_employee_document_by_id(self, employee_id: int, document_id: int) -> EmployeeDocumentResponse:
        db_employee_document = (
            await self.document_repository.get_employee_document_by_id(document_id)
        )
        if not db_employee_document:
            raise EmployeeDocumentNotFoundException()
        return EmployeeDocumentResponse.model_validate(db_employee_document)

    async def get_employee_documents(
        self, page: int, limit: int, employee_id: int
    ) -> PaginatedResponse[EmployeeDocumentResponse]:
        skip = (page - 1) * limit
        db_employee_documents, total_rows = (
            await self.document_repository.get_employee_documents(
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
        try:
            document_url, public_id = upload_file(employee_document_data.file, "documents")
            data = employee_document_data.model_dump()
            data.pop("file")
            data.update({"url": document_url, "public_id": public_id})
            db_employee_document = (
                await self.document_repository.create_employee_document(data)
            )
            return EmployeeDocumentResponse.model_validate(db_employee_document)
        except Exception as e:
            raise EmployeeDocumentUploadFailedException()
        
    async def update_employee_document(
        self, employee_id: int, document_id: int, employee_document_data: EmployeeDocumentUpdate
    ) -> EmployeeDocumentResponse:
        db_employee_document = (
            await self.document_repository.get_employee_document_by_id(document_id)
        )
        if not db_employee_document:
            raise EmployeeDocumentNotFoundException()
        try:
            document_url, public_id = upload_file(employee_document_data.file, "documents")
            data = employee_document_data.model_dump()
            data.pop("file")
            data.update({"url": document_url, "public_id": public_id})
            db_employee_document = (
                await self.document_repository.update_employee_document(document_id, data)
            )
            return EmployeeDocumentResponse.model_validate(db_employee_document)
        except Exception as e:
            raise EmployeeDocumentUploadFailedException()

    async def delete_employee_document(self, employee_id: int, document_id: int) -> None:        
        db_employee_document = (
            await self.document_repository.get_employee_document_by_id(document_id)
        )
        if not db_employee_document:
            raise EmployeeDocumentNotFoundException()
        await self.document_repository.delete_employee_document(document_id)

