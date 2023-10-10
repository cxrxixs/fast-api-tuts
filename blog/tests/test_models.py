from sqlalchemy.orm import Session

from .. import crud, schemas


def test_create_blog(db_session: Session, blog_factory):
    blog_factory(title="Blog test")
    blog = crud.get_blog(db=db_session, blog_id=1)

    assert blog
    assert "Blog test" == blog.title


def test_model_repr(db_session: Session, blog_factory):
    blog_factory()
    blog = crud.get_blog(db=db_session, blog_id=1)

    assert blog
    assert isinstance(repr(blog), str)
