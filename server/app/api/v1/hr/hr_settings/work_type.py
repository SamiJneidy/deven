from math import ceil
from fastapi import APIRouter, status, Query
from app.schemas.user import UserResponse
from app.schemas import SignleObjectResponse, PaginatedResponse, WorkTypeCreate, WorkTypeUpdate, WorkTypeResponse
from app.services import WorkTypeService
from app.core.dependencies import (
    Annotated, 
    Depends, 
    get_work_type_service,
    get_current_user
)

router = APIRouter(
    prefix="/work-types", 
    tags=["Work Types"],
)


@router.get(
    path="/", 
    response_model=PaginatedResponse[WorkTypeResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The work types has been returned successfully."
        },
    }
)
async def get_work_types(
    work_type_service: Annotated[WorkTypeService, Depends(get_work_type_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
) -> PaginatedResponse[WorkTypeResponse]:
    """Get all work types."""
    return await work_type_service.get_work_types(page, limit)

@router.get(
    path="/{id}", 
    response_model=SignleObjectResponse[WorkTypeResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The work type has been returned successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The work type was not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "WorkTypeNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Work type not found."
                            }
                        },
                    }
                }
            }
        },
    }
)
async def get_work_type(
    id: int,
    work_type_service: Annotated[WorkTypeService, Depends(get_work_type_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> SignleObjectResponse[WorkTypeResponse]:
    """Get work type by id.""" 
    data = await work_type_service.get_work_type_by_id(id)
    return SignleObjectResponse[WorkTypeResponse](data=data)


@router.post(
    path="/", 
    response_model=SignleObjectResponse[WorkTypeResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The work type has been created successfully."
        },
    }
)
async def create_work_type(
    work_type_data: WorkTypeCreate,
    work_type_service: Annotated[WorkTypeService, Depends(get_work_type_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> SignleObjectResponse[WorkTypeResponse]:
    """Create a new work type.""" 
    data = await work_type_service.create_work_type(work_type_data)
    return SignleObjectResponse[WorkTypeResponse](data=data)


@router.put(
    path="/{id}", 
    response_model=SignleObjectResponse[WorkTypeResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The work type has been updated successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The work type was not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "WorkTypeNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Work type not found."
                            }
                        },
                    }
                }
            }
        },
    }
)
async def update_work_type(
    id: int,
    work_type_data: WorkTypeUpdate,
    work_type_service: Annotated[WorkTypeService, Depends(get_work_type_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> SignleObjectResponse[WorkTypeResponse]:
    """Update work type info.""" 
    data = await work_type_service.update_work_type(id, work_type_data)
    return SignleObjectResponse[WorkTypeResponse](data=data)


@router.delete(
    path="/{id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "The work type has been deleted successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The work type was not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "WorkTypeNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Work type not found."
                            }
                        },
                    }
                }
            }
        },
    }
)
async def delete_work_type(
    id: int,
    work_type_service: Annotated[WorkTypeService, Depends(get_work_type_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> None:
    """Delete work type.""" 
    await work_type_service.delete_work_type(id)
    return