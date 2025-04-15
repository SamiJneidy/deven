from pydantic import BaseModel

class BaseAppExceptionSchema(BaseModel):
    """Base exception schema for OpenAPI documentaion."""
    code: int
    message: str