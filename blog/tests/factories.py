import factory
from database import SessionLocal

from ..models import Blog


class BlogFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Blog
        sqlalchemy_session = SessionLocal()
        sqlalchemy_session_persistence = "commit"

    title = "Blog title"
    body = "Blog body "
