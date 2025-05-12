from fastapi import APIRouter, status
from app.schemas import SignleObjectResponse, CompanyCreate, CompanyUpdate, CompanyResponse
from app.services import CompanyService
from app.core.dependencies import (
    Annotated, 
    Depends, 
    get_company_service,
)

router = APIRouter(
    prefix="/company", 
    tags=["Company"],
)


@router.get(
    path="/{id}", 
    response_model=SignleObjectResponse[CompanyResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The company has been returned successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The company was not found.",
            "content": {
                "application/json": {
                    "exmpales": {
                        "CompanyNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Company not found."
                            }
                        },
                    }
                }
            }
        },
    }
)
async def get_company(
    id: int,
    company_service: Annotated[CompanyService, Depends(get_company_service)],
) -> SignleObjectResponse[CompanyResponse]:
    """Get company by id.""" 
    data = await company_service.get_company_by_id(id)
    return SignleObjectResponse[CompanyResponse](data=data)

@router.post(
    path="/", 
    response_model=SignleObjectResponse[CompanyResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The company has been created successfully."
        },
    }
)
async def create_company(
    company_data: CompanyCreate,
    company_service: Annotated[CompanyService, Depends(get_company_service)],
) -> SignleObjectResponse[CompanyResponse]:
    """Create a new company after signup.""" 
    data = await company_service.create_company(company_data)
    return SignleObjectResponse[CompanyResponse](data=data)


@router.put(
    path="/{id}", 
    response_model=SignleObjectResponse[CompanyResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The company has been updated successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The company was not found.",
            "content": {
                "application/json": {
                    "exmpales": {
                        "CompanyNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Company not found."
                            }
                        },
                    }
                }
            }
        },
    }
)
async def update_company(
    id: int,
    company_data: CompanyUpdate,
    company_service: Annotated[CompanyService, Depends(get_company_service)],
) -> SignleObjectResponse[CompanyResponse]:
    """Update company info.""" 
    data = await company_service.update_company(id, company_data)
    return SignleObjectResponse[CompanyResponse](data=data)
