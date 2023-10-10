import pytest
from fastapi import HTTPException
from psycopg2.errors import (ForeignKeyViolation, RestrictViolation,
                             UniqueViolation)
from pytest import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import crud, schemas


def test_create_blog_integrity_error(db_session: Session, mocker):
    mocker.patch.object(
        db_session,
        "commit",
        side_effect=IntegrityError("", "", RestrictViolation()),
    )

    new_blog = schemas.BlogCreate(
        title="Test blog title",
        body="Test blog body",
    )

    with pytest.raises(IntegrityError) as exc_info:
        crud.create_blog(db_session, new_blog, author_id=1)

    assert not isinstance(exc_info.value.orig, UniqueViolation)


def test_create_blog_http_exception(db_session: Session, mocker):
    mocker.patch.object(
        db_session,
        "commit",
        side_effect=IntegrityError(
            "",
            "",
            UniqueViolation(),
        ),
    )

    new_blog = schemas.BlogCreate(title="Test blog title", body="Test blog body")

    with pytest.raises(HTTPException) as exc_info:
        crud.create_blog(db_session, new_blog, author_id=1)

    assert exc_info.value.status_code == 400


def test_create_blog_foreignkey_violation(db_session: Session):
    INVALID_AUTHOR_ID = 9999
    with pytest.raises(HTTPException) as exc_info:
        new_blog = schemas.BlogCreate(title="Test blog title", body="Test blog boy")
        crud.create_blog(db_session, new_blog, author_id=INVALID_AUTHOR_ID)

    assert exc_info.value.status_code == 400


def test_update_blog_integrity_error(
    db_session: Session,
    mocker,
    blog_factory,
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

    update_info = schemas.BlogUpdate(title="Update blog title")

    with pytest.raises(IntegrityError) as exc_info:
        blog_factory()
        crud.update_blog(db_session, 1, update_info)

    assert isinstance(exc_info.value.orig, RestrictViolation)
