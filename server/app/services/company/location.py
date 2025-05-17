from app.repositories import LocationRepository
from app.schemas.company import LocationCreate, LocationUpdate, LocationResponse
from app.core.exceptions.company import LocationNotFoundException

class LocationService:
    def __init__(self, location_repository: LocationRepository) -> None:
        self.location_repository = location_repository

    async def get_location_by_id(self, id: int) -> LocationResponse:
        db_location = await self.location_repository.get_location_by_id(id)
        if not db_location:
            raise LocationNotFoundException()
        return LocationResponse.model_validate(db_location)

    async def get_locations(self, skip: int, limit: int) -> list[LocationResponse]:
        db_locations = await self.location_repository.get_locations(skip, limit)
        locations = [LocationResponse.model_validate(db_location) for db_location in db_locations]
        return locations

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
