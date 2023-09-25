# client = TestClient(app)
# import pytest
import pytest
from starlette.testclient import TestClient


def test_ping(test_app: TestClient):
    """Test `index` endpoint

    GIVEN: Index endpoint `/`
    WHEN: `GET` request to endpoint
    THEN: Response status code should be `200`
    """
    response = test_app.get("/")
    assert response.status_code == 200
    assert "Welcome to fastAPI Tutorial" in response.text


def test_welcome_message(test_app: TestClient):
    """Test welcome message

    GIVEN: Index endpoint `/`
    WHEN: `GET` request to endpoint
    THEN: Response should contain string `Welcome to fastAPI Tutorial`
    """
    response = test_app.get("/")
    assert "Welcome to fastAPI Tutorial" in response.text


# @pytest.mark.skip(reason="Test skipping the test")
def test_blog(test_app: TestClient):
    """Test `blog` endpoint"""
    response = test_app.get("/blog")
    assert response.status_code == 200
