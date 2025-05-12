from fastapi import APIRouter
from app.api.v1.authentication import authentication_router
from app.api.v1.company import company_router
from app.api.v1.hr import work_type_router

router = APIRouter()
router.include_router(authentication_router)
router.include_router(company_router)
router.include_router(work_type_router)
