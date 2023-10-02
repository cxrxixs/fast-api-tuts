import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from config import settings
from database import Base
from main import app
from user import models, schemas

# load_dotenv(".env.test")


# Define your test database URL
# DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/fast_api_demo_test"

DATABASE_URL = settings.DATABASE_URL


# SQLAlchemy engine for the test database
@pytest.fixture(scope="function")
def db_session():
    # debug
    print("DATABASE_URL*****", settings.DATABASE_URL)
    print("password", settings.POSTGRES_PASSWORD)
    print("user", settings.POSTGRES_USER)
    print("db_name", settings.POSTGRES_DB_NAME)

    engine = create_engine(DATABASE_URL)

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
