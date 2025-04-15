from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .service_exceptions import BaseAppException

async def base_exception_handler(request: Request, exc: BaseAppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.message
        }
    )