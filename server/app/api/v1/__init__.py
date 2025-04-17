from fastapi import APIRouter
from .authentication import router as auth_router

router = APIRouter()
router.include_router(auth_router)
