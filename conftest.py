import pytest
from fastapi.testclient import TestClient
from pytest_factoryboy import register
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from blog.tests.factories import BlogFactory
from config import settings
from database import Base
from main import app
from user import models
from user.tests.factories import UserFactory

# region Register factory
register(UserFactory)
register(BlogFactory)
# endregion


# SQLAlchemy engine for the test database
@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(settings.DATABASE_URL)

    # Establish a database connection
    connection = engine.connect()

    # Begin a transaction
    transaction = connection.begin()

    # Create a session for database operations
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # Create database tables
        Base.metadata.create_all(bind=engine)
        yield db
    finally:
        # Roll back the transaction to undo any changes made during the test
        db.close()
        transaction.rollback()
        connection.close()

        # Drop the database tables
        Base.metadata.drop_all(bind=engine)


# Use the FastAPI TestClient for making HTTP requests to your app
@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def create_user_fixture(db_session):
    new_user = models.User(email="test_email@mail.com", password="testpassword")
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)


@pytest.fixture(scope="function")
def create_and_delete_user(db_session):
    # Create a user
    new_user = models.User(email="test@mail.com", hashed_password="testpassword")

    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    yield new_user

    # Delete the user after the test
    db_session.query(models.User).filter_by(id=new_user.id).delete()


@pytest.fixture
def mock_db_session(mocker):
    return mocker.patch("database.SessionLocal")
