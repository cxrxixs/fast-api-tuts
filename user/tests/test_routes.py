import pytest
from sqlalchemy.orm import Session
from starlette.testclient import TestClient
from user import crud


class TestRoutes:
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

    @pytest.mark.skip(reason="Test skipping the test")
    def test_blog(self, test_client: TestClient):
        """Test `blog` endpoint"""
        response = test_client.get("/blog")
        assert response.status_code == 200

    def test_add_user(self, test_client: TestClient, db_session: Session):
        new_user = {
            "email": "added_user@test.com",
            "password": "testpassword",
        }

        response = test_client.post("/api/user/", json=new_user)
        assert response.status_code == 200

        response_json = response.json()
        assert response_json["email"] == new_user["email"]
        assert response_json["is_active"] == True

        user = crud.get_user_by_email(db_session, email=new_user["email"])
        assert user
        assert new_user["email"] == user.email

    def test_add_existing_user(
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
