from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete, func
from app.models import Location

class LocationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_location_by_id(self, id: int) -> Location | None:
        return self.db.query(Location).filter(Location.id == id).first()

    async def get_locations(self, skip: int, limit: int) -> tuple[list[Location], int]:
        data = self.db.query(Location).offset(skip).limit(limit).all()
        total_rows = self.db.execute(select(func.count(Location.id))).scalar()
        return data, total_rows


    async def create_location(self, data: dict) -> Location:
        db_location = Location(**data)
        self.db.add(db_location)
        self.db.commit()
        self.db.refresh(db_location)
        return db_location

    async def update_location(self, id: int, data: dict) -> Location:
        self.db.execute(update(Location).where(Location.id==id).values(**data))
        self.db.commit()
        return await self.get_location_by_id(id)
    
    async def delete_location(self, id: int) -> None:
        self.db.execute(delete(Location).where(Location.id==id))
        self.db.commit()
