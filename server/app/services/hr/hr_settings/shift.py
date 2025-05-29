from math import ceil
from app.repositories import ShiftRepository
from app.schemas.hr import ShiftCreate, ShiftUpdate, ShiftResponse
from app.schemas.common import PaginatedResponse
from app.core.exceptions.service_exceptions import ShiftNotFoundException

class ShiftService:
    def __init__(self, shift_repository: ShiftRepository) -> None:
        self.shift_repository = shift_repository

    async def get_shift_by_id(self, id: int) -> ShiftResponse:
        db_shift = await self.shift_repository.get_shift_by_id(id)
        if not db_shift:
            raise ShiftNotFoundException()
        return ShiftResponse.model_validate(db_shift)

    async def get_shifts(self, page: int, limit: int) -> PaginatedResponse[ShiftResponse]:
        skip = (page - 1) * limit
        db_shifts, total_rows = await self.shift_repository.get_shifts(skip, limit)
        shifts = [ShiftResponse.model_validate(db_shift) for db_shift in db_shifts]
        pages = ceil(total_rows / limit)
        return PaginatedResponse[ShiftResponse](
            data=shifts,
            total_rows=total_rows,
            total_pages=pages,
            current_page=page,
            limit=limit
        )

    async def create_shift(self, shift_data: ShiftCreate) -> ShiftResponse:
        db_shift = await self.shift_repository.create_shift(shift_data.model_dump())
        return ShiftResponse.model_validate(db_shift)

    async def update_shift(self, id: int, shift_data: ShiftUpdate) -> ShiftResponse:
        db_shift = await self.shift_repository.get_shift_by_id(id)
        if not db_shift:
            raise ShiftNotFoundException()
        db_shift = await self.shift_repository.update_shift(id, shift_data.model_dump())
        return ShiftResponse.model_validate(db_shift)

    async def delete_shift(self, id: int) -> None:
        db_shift = await self.shift_repository.get_shift_by_id(id)
        if not db_shift:
            raise ShiftNotFoundException()
        await self.shift_repository.delete_shift(id)
