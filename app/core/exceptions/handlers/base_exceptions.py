from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.main import app
from app.core.exceptions.base_exceptions import (
    BaseAppException,
    ResourceNotFoundError, 
    ResourceAlreadyInUseError, 
)

@app.exception_handler(BaseAppException)
async def base_exception_handler(request: Request, exc: BaseAppException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": exc.detail
        }
    )

@app.exception_handler(ResourceNotFoundError)
async def user_not_found_handler(request: Request, exc: ResourceNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "code": status.HTTP_404_NOT_FOUND,
            "message": exc.detail
        }
    )

@app.exception_handler(ResourceAlreadyInUseError)
async def user_not_found_handler(request: Request, exc: ResourceAlreadyInUseError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "code": status.HTTP_409_CONFLICT,
            "message": exc.detail
        }
    )