from math import ceil
from fastapi import APIRouter, status, Query
from app.schemas.user import UserResponse
from app.schemas import SignleObjectResponse, PaginatedResponse, LocationCreate, LocationUpdate, LocationResponse
from app.services import LocationService
from app.core.dependencies import (
    Annotated, 
    Depends, 
    get_location_service,
    get_current_user
)

router = APIRouter(
    prefix="/locations", 
    tags=["Locations"],
)


@router.get(
    path="/", 
    response_model=PaginatedResponse[LocationResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The locations has been returned successfully."
        },
    }
)
async def get_locations(
    location_service: Annotated[LocationService, Depends(get_location_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
) -> PaginatedResponse[LocationResponse]:
    """Get all locations."""
    return await location_service.get_locations(page, limit)


@router.get(
    path="/{id}", 
    response_model=SignleObjectResponse[LocationResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The location has been returned successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The location was not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "LocationNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Location not found."
                            }
                        },
                    }
                }
            }
        },
    }
)
async def get_location(
    id: int,
    location_service: Annotated[LocationService, Depends(get_location_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> SignleObjectResponse[LocationResponse]:
    """Get location by id.""" 
    data = await location_service.get_location_by_id(id)
    return SignleObjectResponse[LocationResponse](data=data)


@router.post(
    path="/", 
    response_model=SignleObjectResponse[LocationResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The location has been created successfully."
        },
    }
)
async def create_location(
    location_data: LocationCreate,
    location_service: Annotated[LocationService, Depends(get_location_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> SignleObjectResponse[LocationResponse]:
    """Create a new location.""" 
    data = await location_service.create_location(location_data)
    return SignleObjectResponse[LocationResponse](data=data)


@router.put(
    path="/{id}", 
    response_model=SignleObjectResponse[LocationResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The location has been updated successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The location was not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "LocationNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Location not found."
                            }
                        },
                    }
                }
            }
        },
    }
)
async def update_location(
    id: int,
    location_data: LocationUpdate,
    location_service: Annotated[LocationService, Depends(get_location_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> SignleObjectResponse[LocationResponse]:
    """Update location info.""" 
    data = await location_service.update_location(id, location_data)
    return SignleObjectResponse[LocationResponse](data=data)


@router.delete(
    path="/{id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "The location has been deleted successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The location was not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "LocationNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Location not found."
                            }
                        },
                    }
                }
            }
        },
    }
)
async def delete_location(
    id: int,
    location_service: Annotated[LocationService, Depends(get_location_service)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> None:
    """Delete location.""" 
    await location_service.delete_location(id)
    return