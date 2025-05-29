import json
from math import ceil
from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    Response,
    UploadFile,
    status,
    Query,
)
from fastapi.responses import JSONResponse
from app.schemas.user import UserResponse
from app.schemas import (
    SignleObjectResponse,
    PaginatedResponse,
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    ProfilePicture
)
from app.services import EmployeeService
from app.core.dependencies import (
    Annotated,
    Depends,
    get_employee_service,
    get_current_user,
)

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)


@router.get(
    path="/",
    response_model=PaginatedResponse[EmployeeResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The employee has been returned successfully."
        },
    },
)
async def get_employees(
    employee_service: Annotated[EmployeeService, Depends(get_employee_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
) -> PaginatedResponse[EmployeeResponse]:
    """Get all employees."""
    return await employee_service.get_employees(page, limit)


@router.get(
    path="/{id}",
    response_model=SignleObjectResponse[EmployeeResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The employee has been returned successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The employee was not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "EmployeeNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Employee not found.",
                            }
                        },
                    }
                }
            },
        },
    },
)
async def get_employee(
    id: int,
    employee_service: Annotated[EmployeeService, Depends(get_employee_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> SignleObjectResponse[EmployeeResponse]:
    """Get employee by id."""
    data = await employee_service.get_employee_by_id(id)
    return SignleObjectResponse[EmployeeResponse](data=data)


@router.post(
    path="/",
    response_model=SignleObjectResponse[EmployeeResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The employee has been created successfully."
        },
    },
)
async def create_employee(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    employee_service: Annotated[EmployeeService, Depends(get_employee_service)],
    employee_data: EmployeeCreate,
) -> SignleObjectResponse[EmployeeResponse]:
    """Create a new employee."""
    data = await employee_service.create_employee(employee_data)
    return SignleObjectResponse[EmployeeResponse](data=data)


@router.put(
    path="/{id}",
    response_model=SignleObjectResponse[EmployeeResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The employee has been updated successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The employee was not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "EmployeeNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Employee not found.",
                            }
                        },
                    }
                }
            },
        },
    },
)
async def update_employee(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    employee_service: Annotated[EmployeeService, Depends(get_employee_service)],
    employee_data: EmployeeUpdate,
    id: int,
) -> SignleObjectResponse[EmployeeResponse]:
    """Update employee info."""
    data = await employee_service.update_employee(id, employee_data)
    return SignleObjectResponse[EmployeeResponse](data=data)


@router.delete(
    path="/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "The employee has been deleted successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The employee was not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "EmployeeNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Employee not found.",
                            }
                        },
                    }
                }
            },
        },
    },
)
async def delete_employee(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    employee_service: Annotated[EmployeeService, Depends(get_employee_service)],
    id: int,
) -> None:
    """Delete employee."""
    await employee_service.delete_employee(id)
    return


@router.post(
    path="/{id}/profile-picture",
    status_code=status.HTTP_200_OK,
    response_model=ProfilePicture,
    responses={
        status.HTTP_200_OK: {
            "description": "The profile picture has been uploaded successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The employee was not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "EmployeeNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Employee not found.",
                            }
                        },
                    }
                }
            },
        },
    },
)
async def upload_profile_picture(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    employee_service: Annotated[EmployeeService, Depends(get_employee_service)],
    id: int,
    image: UploadFile = File(...),
) -> ProfilePicture:
    """Update employee info."""
    return await employee_service.upload_profile_picture(id, image)


@router.delete(
    path="/{id}/profile-picture",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "The profile picture has been deleted successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The employee was not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "EmployeeNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Employee not found.",
                            }
                        },
                    }
                }
            },
        },
    },
)
async def remove_profile_picture(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    employee_service: Annotated[EmployeeService, Depends(get_employee_service)],
    id: int,
) -> None:
    """Remove profile picture for an employee."""
    await employee_service.remove_profile_picture(id)
    return
