import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi_docx.openapi import custom_openapi
from .core.exceptions.exception_handlers import base_exception_handler
from .core.exceptions.service_exceptions import BaseAppException
from .core.exceptions.exception_schemas import BaseAppExceptionSchema
from .services.base import BaseService
from .api.v1.authentication import router

app = FastAPI()
app.include_router(router)

@app.exception_handler(BaseAppException)
async def app_exception_handler(request, e):
    return await base_exception_handler(request, e)

app.openapi = custom_openapi(
    app,
    customError=BaseAppException,
    customErrSchema=BaseAppExceptionSchema,
    serviceClasses=(BaseService,)
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("server.app.main:app", host="0.0.0.0", port=8000, reload=True)