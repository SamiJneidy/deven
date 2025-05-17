from app.repositories import ShiftRepository
from app.schemas.hr import ShiftCreate, ShiftUpdate, ShiftResponse
from app.core.exceptions.hr import ShiftNotFoundException

class ShiftService:
    def __init__(self, shift_repository: ShiftRepository) -> None:
        self.shift_repository = shift_repository

    async def get_shift_by_id(self, id: int) -> ShiftResponse:
        db_shift = await self.shift_repository.get_shift_by_id(id)
        if not db_shift:
            raise ShiftNotFoundException()
        return ShiftResponse.model_validate(db_shift)

    async def get_shifts(self, skip: int, limit: int) -> list[ShiftResponse]:
        db_shifts = await self.shift_repository.get_shifts(skip, limit)
        shifts = [ShiftResponse.model_validate(db_shift) for db_shift in db_shifts]
        return shifts

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
