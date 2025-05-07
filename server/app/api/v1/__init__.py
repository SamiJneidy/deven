from fastapi import APIRouter
from .authentication import router as auth_router
from .company import router as company_router
router = APIRouter()
router.include_router(auth_router)
router.include_router(company_router)
