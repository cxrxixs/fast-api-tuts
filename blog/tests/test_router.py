import pytest
from sqlalchemy.orm import Session
from starlette.testclient import TestClient
from user.models import User


class TestRouter:
    def test_ping(self, test_client: TestClient):
        response = test_client.get("/api/blog/")

        assert response.status_code == 200
        assert "Blog index page" in response.text

    @pytest.mark.parametrize(
        "blog_count, status_code",
        [
            (0, 404),
            (2, 200),
        ],
    )
    def test_read_blogs(
        self,
        test_client: TestClient,
        db_session: Session,
        blog_factory,
        user_factory,
        blog_count,
        status_code,
    ):
        if blog_count > 0:
            user_factory()
            user = db_session.query(User).first()

            if user:
                blog_factory(author_id=user.id)
                blog_factory(
                    title="Second blog",
                    body="Second blog",
                    author_id=user.id,
                )

        response = test_client.get("/api/blog/all")

        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "blog_count, status_code",
        [
            (0, 404),
            (1, 200),
        ],
    )
    def test_read_blog(
        self,
        test_client: TestClient,
        db_session: Session,
        blog_factory,
        user_factory,
        blog_count,
        status_code,
    ):
        if blog_count > 0:
            user_factory()
            user = db_session.query(User).first()

            if user:
                blog_factory(author_id=user.id)

        blog_id = blog_count
        response = test_client.get(f"api/blog/{blog_id}")

        assert response.status_code == status_code

    def test_create_blog(
        self,
        test_client: TestClient,
        db_session: Session,  # pyright:ignore
        user_factory,
    ):
        user_factory()

        new_blog = {
            "title": "Test blog",
            "body": "Blog body",
        }

        response = test_client.post("/api/blog/?author_id=1", json=new_blog)
        print(response.json())

        assert response.status_code == 200

    @pytest.mark.parametrize(
        "blog_id, status_code",
        [
            (1, 200),
            (999, 404),
        ],
    )
    def test_update_blog(
        self,
        db_session: Session,  # pyright:ignore
        test_client: TestClient,
        user_factory,
        blog_factory,
        blog_id,
        status_code,
    ):
        user_factory()
        blog_factory(author_id=1)
        blog_info = {"title": "Modified title"}

        response = test_client.put(f"api/blog/{blog_id}", json=blog_info)

        assert response.status_code == status_code
