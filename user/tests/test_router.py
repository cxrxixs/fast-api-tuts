import pytest
from sqlalchemy.orm import Session
from starlette.testclient import TestClient
from user import crud


class TestRouter:
    def test_ping(self, test_client: TestClient):
        """Test `index` endpoint

        GIVEN: Index endpoint `/`
        WHEN: `GET` request to endpoint
        THEN: Response status code should be `200`
        """
        response = test_client.get("/")
        assert response.status_code == 200
        assert "Welcome to fastAPI Tutorial" in response.text

    def test_welcome_message(self, test_client: TestClient):
        """Test welcome message

        GIVEN: Index endpoint `/`
        WHEN: `GET` request to endpoint
        THEN: Response should contain string `Welcome to fastAPI Tutorial`
        """
        response = test_client.get("/")
        assert "Welcome to fastAPI Tutorial" in response.text

    @pytest.mark.skip(reason="This is how to skip a test")
    def test_blog(self, test_client: TestClient):
        """Test `blog` endpoint"""
        response = test_client.get("/blog")
        assert response.status_code == 200

    def test_create_user(self, test_client: TestClient, db_session: Session):
        new_user = {
            "email": "added_user@test.com",
            "password": "testpassword",
        }

        response = test_client.post("/api/user/", json=new_user)
        assert response.status_code == 200

        response_json = response.json()
        assert response_json["email"] == new_user["email"]
        assert response_json["is_active"]

        user = crud.get_user_by_email(db_session, email=new_user["email"])
        assert user
        assert new_user["email"] == user.email

    def test_create_existing_user(
        self,
        test_client: TestClient,
        db_session: Session,
        user_factory,
    ):
        user_factory()

        new_user = {
            "email": "test@mail.com",
            "password": "testpassword",
        }

        response = test_client.post("/api/user/", json=new_user)
        assert response.status_code == 400
        assert response.json()["detail"] == "User already exists"

        user = crud.get_user_by_email(db_session, email=new_user["email"])
        assert user
        assert new_user["email"] == user.email

    @pytest.mark.parametrize(
        "user_id, status_code",
        [
            (1, 200),
            (99, 404),
        ],
    )
    def test_read_user(
        self,
        test_client: TestClient,
        db_session: Session,  # pyright:ignore
        user_factory,
        user_id,
        status_code,
    ):
        user_factory()
        response = test_client.get(f"api/user/{user_id}")
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "user_count, status_code",
        [
            (1, 200),
            (0, 404),
        ],
    )
    def test_read_users(
        self,
        test_client: TestClient,
        db_session: Session,  # pyright:ignore
        user_factory,
        user_count,
        status_code,
    ):
        if user_count == 1:
            user_factory()

        response = test_client.get("api/user/")
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "user_id, status_code",
        [
            (1, 200),
            (999, 404),
        ],
    )
    def test_update_user(
        self,
        db_session: Session,  # pyright:ignore
        test_client: TestClient,
        user_factory,
        user_id,
        status_code,
    ):
        user_factory()
        user_info = {"email": "update_email@example.com"}

        response = test_client.put(f"api/user/{user_id}", json=user_info)

        assert response.status_code == status_code
