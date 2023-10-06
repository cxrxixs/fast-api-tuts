from .. import crud, schemas


def test_create_user(db_session):
    payload = schemas.UserCreate(email="test@mail.com", password="testpassword")
    crud.create_user(db_session, payload)
    user = crud.get_user(db_session, user_id=1)

    assert user
    assert "test@mail.com" == user.email


def test_get_user_by_email(db_session, user_factory):
    email = "test_user@example.com"
    user_factory(email=email)
    user = crud.get_user_by_email(db_session, email=email)

    assert user
    assert email == user.email
