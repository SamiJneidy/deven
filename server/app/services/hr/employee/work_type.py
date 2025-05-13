from app.repositories import WorkTypeRepository
from app.schemas.hr import WorkTypeCreate, WorkTypeUpdate, WorkTypeResponse
from app.core.exceptions.hr import WorkTypeNotFound

class WorkTypeService:
    def __init__(self, work_type_repository: WorkTypeRepository) -> None:
        self.work_type_repository = work_type_repository

    async def get_work_type_by_id(self, id: int) -> WorkTypeResponse:
        db_work_type = await self.work_type_repository.get_work_type_by_id(id)
        if not db_work_type:
            raise WorkTypeNotFound()
        return WorkTypeResponse.model_validate(db_work_type)

    async def get_work_types(self, skip: int, limit: int) -> list[WorkTypeResponse]:
        db_work_types = await self.work_type_repository.get_work_types(skip, limit)
        work_types = [WorkTypeResponse.model_validate(db_work_type) for db_work_type in db_work_types]
        return work_types

    async def create_work_type(self, work_type_data: WorkTypeCreate) -> WorkTypeResponse:
        db_work_type = await self.work_type_repository.create_work_type(work_type_data.model_dump())
        return WorkTypeResponse.model_validate(db_work_type)

    async def update_work_type(self, id: int, work_type_data: WorkTypeUpdate) -> WorkTypeResponse:
        db_work_type = await self.work_type_repository.get_work_type_by_id(id)
        if not db_work_type:
            raise WorkTypeNotFound()
        db_work_type = await self.work_type_repository.update_work_type(id, work_type_data.model_dump())
        return WorkTypeResponse.model_validate(db_work_type)

    async def delete_work_type(self, id: int) -> None:
        db_work_type = await self.work_type_repository.get_work_type_by_id(id)
        if not db_work_type:
            raise WorkTypeNotFound()
        await self.work_type_repository.delete_work_type(id)
