import json

import pytest

# from starlette.testclient import TestClient
from .. import crud, schemas

# from database import SessionLocal


# db = SessionLocal()


def test_create_user(db_session):
    payload = schemas.UserCreate(email="test@mail.com", password="testpassword")
    crud.create_user(db_session, payload)

    user = crud.get_user(db_session, 1)
    assert user.email == "test@mail.com"

    user = crud.get_user_by_email(db_session, "test@mail.com")
    assert user.email == "test@mail.com"

    users = crud.get_users(db_session)
    assert len(users) == 1
