from fastapi import APIRouter

from .router import router as blog_router

router = APIRouter()

router.include_router(blog_router, tags=["BLOG"], prefix="/api/blog")
