from fastapi import APIRouter
from app.api.v1.authentication import authentication_router
from app.api.v1.company import company_router, department_router, location_router
from app.api.v1.hr import (
    work_type_router,
    job_title_router,
    shift_router,
    employee_education_router,
    employee_router,
)

router = APIRouter()
router.include_router(authentication_router)
router.include_router(company_router)
router.include_router(work_type_router)
router.include_router(job_title_router)
router.include_router(department_router)
router.include_router(shift_router)
router.include_router(location_router)
router.include_router(employee_education_router)
router.include_router(employee_router)
