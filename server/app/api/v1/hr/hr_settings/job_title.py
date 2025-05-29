from math import ceil
from fastapi import APIRouter, status, Query
from app.schemas.user import UserResponse
from app.schemas import SignleObjectResponse, PaginatedResponse, JobTitleCreate, JobTitleUpdate, JobTitleResponse
from app.services import JobTitleService
from app.core.dependencies import (
    Annotated, 
    Depends, 
    get_job_title_service,
    get_current_user
)

router = APIRouter(
    prefix="/job-titles", 
    tags=["Job Titles"],
)


@router.get(
    path="/", 
    response_model=PaginatedResponse[JobTitleResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The job titles has been returned successfully."
        },
    }
)
async def get_job_titles(
    job_title_service: Annotated[JobTitleService, Depends(get_job_title_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
) -> PaginatedResponse[JobTitleResponse]:
    """Get all job titles."""
    return await job_title_service.get_job_titles(page, limit)


@router.get(
    path="/{id}", 
    response_model=SignleObjectResponse[JobTitleResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The job title has been returned successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The job title was not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "JobTitleNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Job title not found."
                            }
                        },
                    }
                }
            }
        },
    }
)
async def get_job_title(
    id: int,
    job_title_service: Annotated[JobTitleService, Depends(get_job_title_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> SignleObjectResponse[JobTitleResponse]:
    """Get job title by id.""" 
    data = await job_title_service.get_job_title_by_id(id)
    return SignleObjectResponse[JobTitleResponse](data=data)


@router.post(
    path="/", 
    response_model=SignleObjectResponse[JobTitleResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The job title has been created successfully."
        },
    }
)
async def create_job_title(
    job_title_data: JobTitleCreate,
    job_title_service: Annotated[JobTitleService, Depends(get_job_title_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> SignleObjectResponse[JobTitleResponse]:
    """Create a new job title.""" 
    data = await job_title_service.create_job_title(job_title_data)
    return SignleObjectResponse[JobTitleResponse](data=data)


@router.put(
    path="/{id}", 
    response_model=SignleObjectResponse[JobTitleResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The job title has been updated successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The job title was not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "JobTitleNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Job title not found."
                            }
                        },
                    }
                }
            }
        },
    }
)
async def update_job_title(
    id: int,
    job_title_data: JobTitleUpdate,
    job_title_service: Annotated[JobTitleService, Depends(get_job_title_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> SignleObjectResponse[JobTitleResponse]:
    """Update job title info.""" 
    data = await job_title_service.update_job_title(id, job_title_data)
    return SignleObjectResponse[JobTitleResponse](data=data)


@router.delete(
    path="/{id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "The job title has been deleted successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The job title was not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "JobTitleNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Job title not found."
                            }
                        },
                    }
                }
            }
        },
    }
)
async def delete_job_title(
    id: int,
    job_title_service: Annotated[JobTitleService, Depends(get_job_title_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> None:
    """Delete job title.""" 
    await job_title_service.delete_job_title(id)
    return