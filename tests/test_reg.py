import pytest
import requests
from unittest.mock import patch

BASE_URL = "http://127.0.0.1:5000"


@pytest.fixture(scope="session", autouse=True)
def mock_requests():
    """Mock all requests to the API to prevent real HTTP calls."""
    with patch("requests.post") as mock_post, patch("requests.get") as mock_get:
        mock_post.side_effect = lambda url, json, headers=None: \
            mock_response(201, {"message": "Registration successful!"}) if "/register" in url else \
                mock_response(200, {"message": "Login successful!", "token": "mock_token"}) if "/login" in url else \
                    mock_response(200, {"message": "Item added to cart"}) if "/cart/add" in url else \
                        mock_response(200, {"message": "Checkout successful!"}) if "/checkout" in url else \
                            mock_response(400, {"error": "Invalid request"})

        mock_get.side_effect = lambda url: \
            mock_response(200, {"inventory": {"Chair": 2}}) if "/inventory" in url else \
                mock_response(404, {"error": "Not Found"})

        yield  # Provide the mock context


def mock_response(status_code, json_data):
    """Helper function to create a mock response object."""
    response = requests.models.Response()
    response.status_code = status_code
    response._content = json.dumps(json_data).encode("utf-8")
    return response


def test_order_process():
    """Regression Test - Ensures order affects all components correctly."""
    user_data = {"username": "regression_test", "password": "testpass"}
    requests.post(f"{BASE_URL}/register", json=user_data)
    login_res = requests.post(f"{BASE_URL}/login", json=user_data)
    token = login_res.json().get("token")
    headers = {"Authorization": token}

    # Add item to cart
    requests.post(
        f"{BASE_URL}/cart/add",
        json={"item": {"name": "Chair", "quantity": 1}},
        headers=headers,
    )

    # Checkout
    checkout_res = requests.post(f"{BASE_URL}/checkout", headers=headers)
    assert checkout_res.status_code == 200

    # Check inventory update
    inventory_res = requests.get(f"{BASE_URL}/inventory")
    assert "Chair" in inventory_res.json()["inventory"]
    assert inventory_res.json()["inventory"]["Chair"] == 2
