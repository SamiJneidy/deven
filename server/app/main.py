import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.exceptions.handlers import base_exception_handler
from app.core.exceptions.base import BaseAppException
from app.api.v1 import router

app = FastAPI()
app.include_router(router, prefix="/api/v1")

@app.exception_handler(BaseAppException)
async def app_exception_handler(request, e):
    return await base_exception_handler(request, e)

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