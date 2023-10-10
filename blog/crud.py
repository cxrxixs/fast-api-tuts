from fastapi import HTTPException, status
from psycopg2.errors import ForeignKeyViolation, UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import models, schemas


def get_blog(db: Session, blog_id: int) -> models.Blog:
    return db.query(models.Blog).filter(models.Blog.id == blog_id).first()


def get_blogs(db: Session, skip: int = 0, limit: int = 10) -> list[models.Blog]:
    return db.query(models.Blog).offset(skip).limit(limit).all()


def create_blog(db: Session, blog: schemas.BlogCreate, author_id: int) -> models.Blog:
    new_blog = models.Blog(**blog.model_dump(exclude_unset=True), author_id=author_id)
    db.add(new_blog)

    try:
        db.commit()
        db.refresh(new_blog)
        return new_blog

    except IntegrityError as err:
        if isinstance(err.orig, UniqueViolation):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Blog entry already exists",
            )
        elif isinstance(err.orig, ForeignKeyViolation):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user",
            )
        else:
            print(err)
            db.rollback()
            raise


def update_blog(
    db: Session,
    blog_id: int,
    obj_in: schemas.BlogUpdate,
):
    blog = db.query(models.Blog).filter_by(id=blog_id).first()
    if not blog:
        return None

    obj_data = obj_in.model_dump(exclude_unset=True)

    for key, value in obj_data.items():
        setattr(blog, key, value)

    try:
        db.commit()
        db.refresh(blog)
        return blog

    except IntegrityError as err:
        db.rollback()
        print(err)
        raise err
