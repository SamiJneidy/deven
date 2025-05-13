from app.repositories import JobTitleRepository
from app.schemas.hr import JobTitleCreate, JobTitleUpdate, JobTitleResponse
from app.core.exceptions.hr import JobTitleNotFound

class JobTitleService:
    def __init__(self, job_title_repository: JobTitleRepository) -> None:
        self.job_title_repository = job_title_repository

    async def get_job_title_by_id(self, id: int) -> JobTitleResponse:
        db_job_title = await self.job_title_repository.get_job_title_by_id(id)
        if not db_job_title:
            raise JobTitleNotFound()
        return JobTitleResponse.model_validate(db_job_title)

    async def get_job_titles(self) -> list[JobTitleResponse]:
        db_job_titles = await self.job_title_repository.get_job_titles()
        job_titles = [JobTitleResponse.model_validate(db_job_title) for db_job_title in db_job_titles]
        return job_titles

    async def create_job_title(self, job_title_data: JobTitleCreate) -> JobTitleResponse:
        db_job_title = await self.job_title_repository.create_job_title(job_title_data.model_dump())
        return JobTitleResponse.model_validate(db_job_title)

    async def update_job_title(self, id: int, job_title_data: JobTitleUpdate) -> JobTitleResponse:
        db_job_title = await self.job_title_repository.get_job_title_by_id(id)
        if not db_job_title:
            raise JobTitleNotFound()
        db_job_title = await self.job_title_repository.update_job_title(id, job_title_data.model_dump())
        return JobTitleResponse.model_validate(db_job_title)

    async def delete_job_title(self, id: int) -> None:
        db_job_title = await self.job_title_repository.get_job_title_by_id(id)
        if not db_job_title:
            raise JobTitleNotFound()
        await self.job_title_repository.delete_job_title(id)
