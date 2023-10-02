from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
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
    db: Session, db_obj: schemas.Blog, obj_in: schemas.BlogUpdate
) -> models.Blog:
    obj_data = jsonable_encoder(db_obj)

    if isinstance(obj_in, dict):
        update_data = obj_in

    else:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

    try:
        db.commit()
        db.refresh(db_obj)
        return jsonable_encoder(db_obj)

    except IntegrityError as err:
        print(err)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong"
        )
