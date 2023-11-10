from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from . import crud, schemas

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index() -> str:
    return "<h1>Blog index page</h1>"


@router.get("/all", response_model=list[schemas.Blog])
async def read_blogs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    blogs = crud.get_blogs(db, skip=skip, limit=limit)
    if not blogs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No blog entry."
        )

    return blogs


@router.get("/{id}", response_model=schemas.Blog)
async def read_blog(
    id: int,
    db: Session = Depends(get_db),
):
    blog = crud.get_blog(db, blog_id=id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id: {id} not found.",
        )

    return blog


@router.post("/", response_model=schemas.Blog)
def create_blog(
    blog: schemas.BlogCreate,
    author_id: int,
    db: Session = Depends(get_db),
):
    blog = crud.create_blog(db, blog, author_id)

    return blog


@router.put("/{blog_id}", response_model=schemas.Blog)
async def update_blog(
    blog_id: int,
    blog_in: schemas.BlogUpdate,
    db: Session = Depends(get_db),
):
    # blog = crud.get_blog(db, blog_id=blog_in.id)
    updated_blog = crud.update_blog(db, blog_id, blog_in)
    if not updated_blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id: {blog_id} not found.",
        )

    return updated_blog
