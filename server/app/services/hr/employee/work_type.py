from math import ceil
from app.repositories import WorkTypeRepository
from app.schemas.hr import WorkTypeCreate, WorkTypeUpdate, WorkTypeResponse
from app.schemas.common import PaginatedResponse
from app.core.exceptions.hr import WorkTypeNotFoundException

class WorkTypeService:
    def __init__(self, work_type_repository: WorkTypeRepository) -> None:
        self.work_type_repository = work_type_repository

    async def get_work_type_by_id(self, id: int) -> WorkTypeResponse:
        db_work_type = await self.work_type_repository.get_work_type_by_id(id)
        if not db_work_type:
            raise WorkTypeNotFoundException()
        return WorkTypeResponse.model_validate(db_work_type)

    async def get_work_types(self, page: int, limit: int) -> PaginatedResponse[WorkTypeResponse]:
        skip = (page - 1) * limit
        db_work_types, total_rows = await self.work_type_repository.get_work_types(skip, limit)
        work_types = [WorkTypeResponse.model_validate(db_department) for db_department in db_work_types]
        pages = ceil(total_rows / limit)
        return PaginatedResponse[WorkTypeResponse](
            data=work_types,
            total_rows=total_rows,
            total_pages=pages,
            current_page=page,
            limit=limit
        )

    async def create_work_type(self, work_type_data: WorkTypeCreate) -> WorkTypeResponse:
        db_work_type = await self.work_type_repository.create_work_type(work_type_data.model_dump())
        return WorkTypeResponse.model_validate(db_work_type)

    async def update_work_type(self, id: int, work_type_data: WorkTypeUpdate) -> WorkTypeResponse:
        db_work_type = await self.work_type_repository.get_work_type_by_id(id)
        if not db_work_type:
            raise WorkTypeNotFoundException()
        db_work_type = await self.work_type_repository.update_work_type(id, work_type_data.model_dump())
        return WorkTypeResponse.model_validate(db_work_type)

    async def delete_work_type(self, id: int) -> None:
        db_work_type = await self.work_type_repository.get_work_type_by_id(id)
        if not db_work_type:
            raise WorkTypeNotFoundException()
        await self.work_type_repository.delete_work_type(id)
