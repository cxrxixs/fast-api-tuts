from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from blog import crud as blog_crud
from blog import router as blog_router
from config import settings
from database import get_db
from user import router as user_router


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        debug=settings.DEBUG,
    )

    # Register router here
    application.include_router(blog_router)
    application.include_router(user_router)

    return application


app = get_application()

templates = Jinja2Templates(directory="templates")


# Index page
@app.get("/", response_class=HTMLResponse, tags=["HOME"])
async def index():
    return "<h1>Welcome to fastAPI Tutorial</h1>"


@app.get("/blog", response_class=HTMLResponse, tags=["HOME"])
async def blog_main(request: Request, db: Session = Depends(get_db)):
    blogs = blog_crud.get_blogs(db, skip=0, limit=10)
    return templates.TemplateResponse("blog.html", {"request": request, "blogs": blogs})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        port=8881,
        log_level=settings.LOG_LEVEL,
        reload=True,
    )
