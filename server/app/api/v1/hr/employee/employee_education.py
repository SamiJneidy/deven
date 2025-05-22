from math import ceil
from fastapi import APIRouter, status, Query
from app.schemas.user import UserResponse
from app.schemas import SignleObjectResponse, PaginatedResponse, EmployeeEducationCreate, EmployeeEducationUpdate, EmployeeEducationResponse
from app.services import EmployeeEducationService
from app.core.dependencies import (
    Annotated, 
    Depends, 
    get_employee_education_service,
    get_current_user
)

router = APIRouter(
    prefix="/employee-education", 
    tags=["Employee Education"],
)


@router.get(
    path="/", 
    response_model=PaginatedResponse[EmployeeEducationResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The employee educations has been returned successfully."
        },
    }
)
async def get_employee_educations(
    employee_education_service: Annotated[EmployeeEducationService, Depends(get_employee_education_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    employee_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
) -> PaginatedResponse[EmployeeEducationResponse]:
    """Get all employee educations."""
    return await employee_education_service.get_employee_educations(page, limit, employee_id)


@router.get(
    path="/{id}", 
    response_model=SignleObjectResponse[EmployeeEducationResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The employee education has been returned successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The employee education was not found.",
            "content": {
                "application/json": {
                    "exmpales": {
                        "EmployeeEducationNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Employee education not found."
                            }
                        },
                    }
                }
            }
        },
    }
)
async def get_employee_education(
    id: int,
    employee_education_service: Annotated[EmployeeEducationService, Depends(get_employee_education_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> SignleObjectResponse[EmployeeEducationResponse]:
    """Get employee education by id.""" 
    data = await employee_education_service.get_employee_education_by_id(id)
    return SignleObjectResponse[EmployeeEducationResponse](data=data)


@router.post(
    path="/", 
    response_model=SignleObjectResponse[EmployeeEducationResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The employee education has been created successfully."
        },
    }
)
async def create_employee_education(
    employee_education_data: EmployeeEducationCreate,
    employee_education_service: Annotated[EmployeeEducationService, Depends(get_employee_education_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> SignleObjectResponse[EmployeeEducationResponse]:
    """Create a new employee education.""" 
    data = await employee_education_service.create_employee_education(employee_education_data)
    return SignleObjectResponse[EmployeeEducationResponse](data=data)


@router.put(
    path="/{id}", 
    response_model=SignleObjectResponse[EmployeeEducationResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The employee education has been updated successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The employee education was not found.",
            "content": {
                "application/json": {
                    "exmpales": {
                        "EmployeeEducationNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Employee education not found."
                            }
                        },
                    }
                }
            }
        },
    }
)
async def update_employee_education(
    id: int,
    employee_education_data: EmployeeEducationUpdate,
    employee_education_service: Annotated[EmployeeEducationService, Depends(get_employee_education_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> SignleObjectResponse[EmployeeEducationResponse]:
    """Update employee education info.""" 
    data = await employee_education_service.update_employee_education(id, employee_education_data)
    return SignleObjectResponse[EmployeeEducationResponse](data=data)


@router.delete(
    path="/{id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "The employee education has been deleted successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The employee education was not found.",
            "content": {
                "application/json": {
                    "exmpales": {
                        "EmployeeEducationNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Employee education not found."
                            }
                        },
                    }
                }
            }
        },
    }
)
async def delete_employee_education(
    id: int,
    employee_education_service: Annotated[EmployeeEducationService, Depends(get_employee_education_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> None:
    """Delete employee education.""" 
    await employee_education_service.delete_employee_education(id)
    return