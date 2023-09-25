from datetime import datetime
from typing import List

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    id: int
    email: str | None = None
    password: str | None = None


class UserAsAuthor(BaseModel):
    email: str
    is_active: bool


class BlogId(BaseModel):
    id: int


class BlogDetails(BaseModel):
    id: int
    title: str
    body: str
    created_at: datetime


class User(UserBase):
    id: int
    is_active: bool
    blogs: List[BlogId] | None = None

    class Config:
        from_attributes = True


class UserDetail(UserBase):
    id: int
    is_active: bool
    blogs: List[BlogDetails] | None = None

    class Config:
        from_attributes = True
