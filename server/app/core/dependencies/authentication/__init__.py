from app.core.dependencies.authentication.otp import get_otp_repository, get_otp_service
from app.core.dependencies.authentication.authentication import (
    get_authentication_repository,
    get_authentication_service,
    get_current_user,
    get_current_company,
    get_redis,
    oauth2_scheme,
)
