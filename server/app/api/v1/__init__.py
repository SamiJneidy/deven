from fastapi import APIRouter
from .otp import router as otp_router
from .authentication import router as auth_router

router = APIRouter()
router.include_router(otp_router)
router.include_router(auth_router)
