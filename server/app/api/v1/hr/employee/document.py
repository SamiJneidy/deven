from math import ceil
from fastapi import APIRouter, File, Form, UploadFile, status, Query
from app.schemas.user import UserResponse
from app.schemas import (
    EmployeeDocumentCreate,
    EmployeeDocumentResponse,
    EmployeeDocumentUpdate,
    SignleObjectResponse,
    PaginatedResponse,
)
from app.services import EmployeeDocumentService
from app.core.dependencies import (
    Annotated,
    Depends,
    get_current_user,
    get_employee_document_service,
)

router = APIRouter(
    prefix="/employees",
    tags=["Documents"],
)


@router.get(
    path="/{employee_id}/documents",
    response_model=PaginatedResponse[EmployeeDocumentResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The employee documents has been returned successfully."
        },
    },
)
async def get_employee_documents(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    document_service: Annotated[
        EmployeeDocumentService, Depends(get_employee_document_service)
    ],
    employee_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
) -> PaginatedResponse[EmployeeDocumentResponse]:
    """Get all employee documents."""
    return await document_service.get_employee_documents(page, limit, employee_id)


@router.get(
    path="/{employee_id}/documents/{document_id}",
    response_model=SignleObjectResponse[EmployeeDocumentResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The document has been returned successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The employee was not found or the document was not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "EmployeeNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Employee not found.",
                            }
                        },
                        "EmployeeDocumentNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Document not found.",
                            }
                        },
                    }
                }
            },
        },
    },
)
async def get_employee_document(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    document_service: Annotated[
        EmployeeDocumentService, Depends(get_employee_document_service)
    ],
    employee_id: int,
    document_id: int,
) -> SignleObjectResponse[EmployeeDocumentResponse]:
    """Get employee document by id."""
    data = await document_service.get_employee_document_by_id(employee_id, document_id)
    return SignleObjectResponse[EmployeeDocumentResponse](data=data)


@router.post(
    path="/{employee_id}/documents",
    response_model=SignleObjectResponse[EmployeeDocumentResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The document has been created successfully."
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
async def create_employee_document(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    document_service: Annotated[
        EmployeeDocumentService, Depends(get_employee_document_service)
    ],
    employee_id: int,
    file: UploadFile = File(...),
    name: str = Form(...),
) -> SignleObjectResponse[EmployeeDocumentResponse]:
    """Create a new employee document."""
    employee_document_data = EmployeeDocumentCreate(
        name=name, file=file, employee_id=employee_id
    )
    data = await document_service.create_employee_document(
        employee_id, employee_document_data
    )
    return SignleObjectResponse[EmployeeDocumentResponse](data=data)


@router.put(
    path="/{employee_id}/documents/{document_id}",
    response_model=SignleObjectResponse[EmployeeDocumentResponse],
    responses={
        status.HTTP_200_OK: {
            "description": "The document has been updated successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The employee was not found or the document was not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "EmployeeNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Employee not found.",
                            }
                        },
                        "EmployeeDocumentNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Document not found.",
                            }
                        },
                    }
                }
            },
        },
    },
)
async def update_employee_document(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    document_service: Annotated[
        EmployeeDocumentService, Depends(get_employee_document_service)
    ],
    employee_id: int,
    document_id: int,
    file: UploadFile = File(...),
    name: str = Form(...),
) -> SignleObjectResponse[EmployeeDocumentResponse]:
    """Update employee document info."""
    employee_document_data = EmployeeDocumentUpdate(name=name, file=file)
    data = await document_service.update_employee_document(
        employee_id, document_id, employee_document_data
    )
    return SignleObjectResponse[EmployeeDocumentResponse](data=data)


@router.delete(
    path="/{employee_id}/documents/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "The document has been deleted successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The employee was not found or the document was not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "EmployeeNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Employee not found.",
                            }
                        },
                        "EmployeeDocumentNotFound": {
                            "value": {
                                "code": status.HTTP_404_NOT_FOUND,
                                "message": "Document not found.",
                            }
                        },
                    }
                }
            },
        },
    },
)
async def delete_employee_document(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    document_service: Annotated[
        EmployeeDocumentService, Depends(get_employee_document_service)
    ],
    employee_id: int,
    document_id: int,
) -> None:
    """Delete employee document."""
    await document_service.delete_employee_document(employee_id, document_id)
    return
