import datetime

from pydantic import BaseModel
from user.schemas import UserAsAuthor


class BlogBase(BaseModel):
    title: str
    body: str
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None


class BlogCreate(BlogBase):
    pass


class BlogUpdate(BlogBase):
    title: str | None = None
    body: str | None = None


class Blog(BlogBase):
    id: int
    author_id: int | None = None
    author: UserAsAuthor | None = None

    class Config:
        from_attributes = True
