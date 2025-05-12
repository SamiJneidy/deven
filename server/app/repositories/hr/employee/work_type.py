from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from ....models import WorkType, WorkType, JobTitle

class WorkTypeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_work_type_by_id(self, id: int) -> WorkType | None:
        return self.db.query(WorkType).filter(WorkType.id == id).first()

    async def get_work_types(self) -> list[WorkType]:
        return self.db.query(WorkType).all()

    async def create_work_type(self, data: dict) -> WorkType:
        db_work_type = WorkType(**data)
        self.db.add(db_work_type)
        self.db.commit()
        self.db.refresh(db_work_type)
        return db_work_type

    async def update_work_type(self, id: int, data: dict) -> WorkType:
        self.db.execute(update(WorkType).where(WorkType.id==id).values(**data))
        self.db.commit()
        return await self.get_work_type_by_id(id)
    
    async def delete_work_type(self, id: int) -> None:
        self.db.execute(delete(WorkType).where(WorkType.id==id))
        self.db.commit()
