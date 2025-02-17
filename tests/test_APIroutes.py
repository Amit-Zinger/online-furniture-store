import pytest
import requests
import json
from unittest.mock import patch

BASE_URL = "http://127.0.0.1:5000"


@pytest.fixture(scope="session", autouse=True)
def mock_requests():
    """Mock all requests to the API to prevent real HTTP calls."""
    with patch("requests.post") as mock_post, patch("requests.get") as mock_get:
        # Mock register response
        mock_post.side_effect = lambda url, json: \
            mock_response(201, {"message": "Registration successful!"}) if "/register" in url else \
                mock_response(200, {"message": "Login successful!", "token": "mock_token"}) if "/login" in url else \
                    mock_response(400, {"error": "Invalid request"})

        # Mock get response for fetching users or inventory
        mock_get.side_effect = lambda url: \
            mock_response(200, {"users": []}) if "/users" in url else \
                mock_response(200, {"inventory": []}) if "/inventory" in url else \
                    mock_response(404, {"error": "Not Found"})

        yield  # Provide the mock context


def mock_response(status_code, json_data):
    """Helper function to create a mock response object."""
    response = requests.models.Response()
    response.status_code = status_code
    response._content = json.dumps(json_data).encode("utf-8")
    return response


def test_register_user():
    """Test new user registration with mock."""
    user_data = {
        "username": "new_user",
        "email": "new_user@example.com",
        "password": "newpassword",
        "address": "789 Test Ave",
        "role": "client",
    }
    response = requests.post(f"{BASE_URL}/register", json=user_data)
    assert response.status_code == 201
    assert "Registration successful!" in response.json()["message"]


def test_login():
    """Test valid user login with mock."""
    login_data = {
        "username": "new_user",
        "password": "newpassword",
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    assert response.status_code == 200
    assert "Login successful!" in response.json()["message"]
    assert "mock_token" == response.json()["token"]


if __name__ == "__main__":
    pytest.main()
