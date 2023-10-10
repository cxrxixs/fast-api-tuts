import pytest
from psycopg2.errors import RestrictViolation, UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import crud, schemas


def test_create_user_exception_error(db_session: Session, mocker):
    mocker.patch.object(
        db_session,
        "commit",
        side_effect=IntegrityError("", "", RestrictViolation()),
    )

    new_user = schemas.UserCreate(
        email="test@mail.com",
        password="test",
    )

    with pytest.raises(IntegrityError) as exc_info:
        crud.create_user(db_session, new_user)

    assert not isinstance(exc_info.value.orig, UniqueViolation)


def test_update_user_exception_error(
    db_session: Session,
    mocker,
    user_factory,
):
    mocker.patch.object(
        db_session,
        "commit",
        side_effect=IntegrityError(
            "",
            "",
            RestrictViolation(),
        ),
    )

    user_factory()
    user_obj = schemas.UserUpdate(email="update@example.com")

    with pytest.raises(IntegrityError) as exc_info:
        crud.update_user(db_session, 1, user_obj)

    assert isinstance(exc_info.value.orig, RestrictViolation)
