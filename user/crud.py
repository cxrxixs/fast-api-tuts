from fastapi import HTTPException, status
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    new_user = models.User(
        email=user.email, hashed_password=fake_hashed_password
    )
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as err:
        if isinstance(err.orig, UniqueViolation):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists",
            )
        else:
            print(err)
            db.rollback()
            raise err


def update_user(
    db: Session,
    user_id: int,
    obj_in: schemas.UserUpdate,
):
    user = db.query(models.User).filter_by(id=user_id).first()
    if not user:
        return None

    obj_data = obj_in.model_dump(exclude_unset=True)

    for key, value in obj_data.items():
        setattr(user, key, value)

    try:
        db.commit()
        db.refresh(user)
        return user

    except IntegrityError as err:
        db.rollback()
        print(err)
        raise err
