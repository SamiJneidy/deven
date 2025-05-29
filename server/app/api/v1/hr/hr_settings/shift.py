from math import ceil
from fastapi import APIRouter, status, Query
from app.schemas.user import UserResponse
from app.schemas import SignleObjectResponse, PaginatedResponse, ShiftCreate, ShiftUpdate, ShiftResponse
from app.services import ShiftService
from app.core.dependencies import (
    Annotated, 
    Depends, 
    get_shift_service,
    get_current_user
)

router = APIRouter(
    prefix="/shifts", 
    tags=["Shifts"],
)


@router.get(
    path="/", 
    response_model=PaginatedResponse[ShiftResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The shifts has been returned successfully."
        },
    }
)
async def get_shifts(
    shift_service: Annotated[ShiftService, Depends(get_shift_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
) -> PaginatedResponse[ShiftResponse]:
    """Get all shifts.""" 
    return await shift_service.get_shifts(page, limit)


@router.get(
    path="/{id}", 
    response_model=SignleObjectResponse[ShiftResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The shift has been returned successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The shift was not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "ShiftNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Shift not found."
                            }
                        },
                    }
                }
            }
        },
    }
)
async def get_shift(
    id: int,
    shift_service: Annotated[ShiftService, Depends(get_shift_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> SignleObjectResponse[ShiftResponse]:
    """Get shift by id.""" 
    data = await shift_service.get_shift_by_id(id)
    return SignleObjectResponse[ShiftResponse](data=data)


@router.post(
    path="/", 
    response_model=SignleObjectResponse[ShiftResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The shift has been created successfully."
        },
    }
)
async def create_shift(
    shift_data: ShiftCreate,
    shift_service: Annotated[ShiftService, Depends(get_shift_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> SignleObjectResponse[ShiftResponse]:
    """Create a new shift.""" 
    data = await shift_service.create_shift(shift_data)
    return SignleObjectResponse[ShiftResponse](data=data)


@router.put(
    path="/{id}", 
    response_model=SignleObjectResponse[ShiftResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The shift has been updated successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The shift was not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "ShiftNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Shift not found."
                            }
                        },
                    }
                }
            }
        },
    }
)
async def update_shift(
    id: int,
    shift_data: ShiftUpdate,
    shift_service: Annotated[ShiftService, Depends(get_shift_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> SignleObjectResponse[ShiftResponse]:
    """Update shift info.""" 
    data = await shift_service.update_shift(id, shift_data)
    return SignleObjectResponse[ShiftResponse](data=data)


@router.delete(
    path="/{id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "The shift has been deleted successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The shift was not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "ShiftNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Shift not found."
                            }
                        },
                    }
                }
            }
        },
    }
)
async def delete_shift(
    id: int,
    shift_service: Annotated[ShiftService, Depends(get_shift_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> None:
    """Delete shift.""" 
    await shift_service.delete_shift(id)
    return