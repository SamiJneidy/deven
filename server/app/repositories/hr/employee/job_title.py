from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from app.models import JobTitle

class JobTitleRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_job_title_by_id(self, id: int) -> JobTitle | None:
        return self.db.query(JobTitle).filter(JobTitle.id == id).first()

    async def get_job_titles(self, skip: int, limit: int) -> list[JobTitle]:
        return self.db.query(JobTitle).offset(skip).limit(limit).all()

    async def create_job_title(self, data: dict) -> JobTitle:
        db_job_title = JobTitle(**data)
        self.db.add(db_job_title)
        self.db.commit()
        self.db.refresh(db_job_title)
        return db_job_title

    async def update_job_title(self, id: int, data: dict) -> JobTitle:
        self.db.execute(update(JobTitle).where(JobTitle.id==id).values(**data))
        self.db.commit()
        return await self.get_job_title_by_id(id)
    
    async def delete_job_title(self, id: int) -> None:
        self.db.execute(delete(JobTitle).where(JobTitle.id==id))
        self.db.commit()
