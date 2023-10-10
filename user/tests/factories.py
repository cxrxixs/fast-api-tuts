import factory
from database import SessionLocal

from ..models import User


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = SessionLocal()
        sqlalchemy_session_persistence = "commit"

    email = "test@mail.com"
    hashed_password = "hashedpassword"
