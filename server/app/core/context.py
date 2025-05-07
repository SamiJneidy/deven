from contextvars import ContextVar
from ..schemas import UserResponse
current_user: ContextVar[UserResponse | None] = ContextVar("current_user", default=None)