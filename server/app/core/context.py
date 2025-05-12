from contextvars import ContextVar
from app.schemas import UserResponse, CompanyResponse
current_user: ContextVar[UserResponse | None] = ContextVar("current_user", default=None)
company: ContextVar[CompanyResponse | None] = ContextVar("company", default=None)