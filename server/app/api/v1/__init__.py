from fastapi import APIRouter
from .authentication import authentication_router
from .company import company_router
from .hr import work_type_router

router = APIRouter()
router.include_router(authentication_router)
router.include_router(company_router)
router.include_router(work_type_router)
