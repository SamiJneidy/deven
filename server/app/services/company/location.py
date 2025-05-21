from math import ceil
from app.repositories import LocationRepository
from app.schemas.company import LocationCreate, LocationUpdate, LocationResponse
from app.schemas.common import PaginatedResponse
from app.core.exceptions.company import LocationNotFoundException

class LocationService:
    def __init__(self, location_repository: LocationRepository) -> None:
        self.location_repository = location_repository

    async def get_location_by_id(self, id: int) -> LocationResponse:
        db_location = await self.location_repository.get_location_by_id(id)
        if not db_location:
            raise LocationNotFoundException()
        return LocationResponse.model_validate(db_location)

    async def get_locations(self, page: int, limit: int) -> PaginatedResponse[LocationResponse]:
        skip = (page - 1) * limit
        db_locations, total_rows = await self.location_repository.get_locations(skip, limit)
        locations = [LocationResponse.model_validate(db_department) for db_department in db_locations]
        pages = ceil(total_rows / limit)
        return PaginatedResponse[LocationResponse](
            data=locations,
            total_rows=total_rows,
            total_pages=pages,
            current_page=page,
            limit=limit
        )

    async def create_location(self, location_data: LocationCreate) -> LocationResponse:
        db_location = await self.location_repository.create_location(location_data.model_dump())
        return LocationResponse.model_validate(db_location)

    async def update_location(self, id: int, location_data: LocationUpdate) -> LocationResponse:
        db_location = await self.location_repository.get_location_by_id(id)
        if not db_location:
            raise LocationNotFoundException()
        db_location = await self.location_repository.update_location(id, location_data.model_dump())
        return LocationResponse.model_validate(db_location)

    async def delete_location(self, id: int) -> None:
        db_location = await self.location_repository.get_location_by_id(id)
        if not db_location:
            raise LocationNotFoundException()
        await self.location_repository.delete_location(id)
