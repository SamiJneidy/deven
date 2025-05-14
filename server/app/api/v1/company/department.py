from math import ceil
from fastapi import APIRouter, status, Query
from app.schemas.user import UserResponse
from app.schemas import SignleObjectResponse, PaginationResponse, DepartmentCreate, DepartmentUpdate, DepartmentResponse
from app.services import DepartmentService
from app.core.dependencies import (
    Annotated, 
    Depends, 
    get_department_service,
    get_current_user
)

router = APIRouter(
    prefix="/department", 
    tags=["Department"],
)


@router.get(
    path="/", 
    response_model=PaginationResponse[DepartmentResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The departments has been returned successfully."
        },
    }
)
async def get_departments(
    department_service: Annotated[DepartmentService, Depends(get_department_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
) -> PaginationResponse[DepartmentResponse]:
    """Get all departments."""
    skip = (page - 1) * limit
    data = await department_service.get_departments(skip, limit)
    rows = len(data)
    pages = ceil(rows / limit)
    return PaginationResponse[DepartmentResponse](
        data=data,
        total_rows=len(data),
        total_pages=pages,
        current_page=page,
        limit=limit
    )


@router.get(
    path="/{id}", 
    response_model=SignleObjectResponse[DepartmentResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The department has been returned successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The department was not found.",
            "content": {
                "application/json": {
                    "exmpales": {
                        "DepartmentNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Department not found."
                            }
                        },
                    }
                }
            }
        },
    }
)
async def get_department(
    id: int,
    department_service: Annotated[DepartmentService, Depends(get_department_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> SignleObjectResponse[DepartmentResponse]:
    """Get department by id.""" 
    data = await department_service.get_department_by_id(id)
    return SignleObjectResponse[DepartmentResponse](data=data)


@router.post(
    path="/", 
    response_model=SignleObjectResponse[DepartmentResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The department has been created successfully."
        },
    }
)
async def create_department(
    department_data: DepartmentCreate,
    department_service: Annotated[DepartmentService, Depends(get_department_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> SignleObjectResponse[DepartmentResponse]:
    """Create a new department.""" 
    data = await department_service.create_department(department_data)
    return SignleObjectResponse[DepartmentResponse](data=data)


@router.put(
    path="/{id}", 
    response_model=SignleObjectResponse[DepartmentResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The department has been updated successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The department was not found.",
            "content": {
                "application/json": {
                    "exmpales": {
                        "DepartmentNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Department not found."
                            }
                        },
                    }
                }
            }
        },
    }
)
async def update_department(
    id: int,
    department_data: DepartmentUpdate,
    department_service: Annotated[DepartmentService, Depends(get_department_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> SignleObjectResponse[DepartmentResponse]:
    """Update department info.""" 
    data = await department_service.update_department(id, department_data)
    return SignleObjectResponse[DepartmentResponse](data=data)


@router.delete(
    path="/{id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "The department has been deleted successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The department was not found.",
            "content": {
                "application/json": {
                    "exmpales": {
                        "DepartmentNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Department not found."
                            }
                        },
                    }
                }
            }
        },
    }
)
async def delete_department(
    id: int,
    department_service: Annotated[DepartmentService, Depends(get_department_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> None:
    """Delete department.""" 
    await department_service.delete_department(id)
    return