from fastapi import APIRouter

from .router import router as user_router

router = APIRouter()

router.include_router(user_router, tags=["USER"], prefix="/api/user")
