import json

import pytest
from starlette.testclient import TestClient
from user import crud, models, schemas


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

    def test_add_user(self, test_client: TestClient, create_and_delete_user):
        user = {
            "email": "added_user@test.com",
            "password": "testpassword",
        }

        response = test_client.post("/api/user/", json=user)
        assert response.status_code == 200

        response_json = response.json()
        assert response_json["email"] == user["email"]
        assert response_json["is_active"] == True

    def test_add_existing_user(self, test_client: TestClient, create_and_delete_user):
        create_and_delete_user  # pyright:ignore

        user = {
            "email": "test@mail.com",
            "password": "testpassword",
        }

        response = test_client.post("/api/user/", json=user)
        assert response.status_code == 400
        assert response.json()["detail"] == "User already exists"
