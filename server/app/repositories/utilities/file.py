from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete, func
from app.models import File

class FileRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_file_by_id(self, id: int) -> File | None:
        return self.db.query(File).filter(File.id == id).first()
    
    async def get_files(self, skip: int, limit: int) -> tuple[list[File], int]:
        data = self.db.query(File).offset(skip).limit(limit).all()
        total_rows = self.db.execute(select(func.count(File.id))).scalar()
        return data, total_rows

    async def create_file(self, data: dict) -> File:
        db_file = File(**data)
        self.db.add(db_file)
        self.db.commit()
        self.db.refresh(db_file)
        return db_file

    async def update_file(self, id: int, data: dict) -> File:
        self.db.execute(update(File).where(File.id==id).values(**data))
        self.db.commit()
        return await self.get_file_by_id(id)
    
    async def delete_file(self, id: int) -> None:
        self.db.execute(delete(File).where(File.id==id))
        self.db.commit()
