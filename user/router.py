from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, schemas

router = APIRouter()


@router.get("/{user_id}", response_model=schemas.UserDetail)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return users


@router.post("/", response_model=schemas.UserBase)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = crud.create_urser(db, user)

    return new_user
