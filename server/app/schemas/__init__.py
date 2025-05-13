from app.schemas.common import SignleObjectResponse, ObjectListResponse, PaginationResponse
from app.schemas.authentication import (
    TokenPayload,
    TokenResponse,
    SignUp,
    Login,
    PasswordResetRequest,
    PasswordResetResponse,
    PasswordResetOTPRequest,
    PasswordResetOTPResponse,
    OTPCreate, OTPResponse, OTPVerificationRequest, OTPVerificationResponse
)
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse
from app.schemas.hr.employee.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from app.schemas.hr.employee.work_type import WorkTypeCreate, WorkTypeResponse, WorkTypeUpdate
from app.schemas.hr.employee.job_title import JobTitleCreate, JobTitleResponse, JobTitleUpdate