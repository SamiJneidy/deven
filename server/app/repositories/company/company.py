from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from ...models import Company

class CompanyRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_company_by_id(self, id: int) -> Company | None:
        return self.db.query(Company).filter(Company.id == id).first()

    async def create_company(self, data: dict) -> Company:
        db_company = Company(**data)
        self.db.add(db_company)
        self.db.commit()
        self.db.refresh(db_company)
        return db_company

    async def update_company(self, id: int, data: dict) -> Company:
        self.db.execute(update(Company).where(Company.id==id).values(**data))
        self.db.commit()
        return await self.get_company_by_id(id)
    
    async def delete_company(self, id: int) -> None:
        self.db.execute(delete(Company).where(Company.id==id))
        self.db.commit()
