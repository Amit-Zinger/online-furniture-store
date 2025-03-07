import pytest
import requests
import json
from unittest.mock import patch

BASE_URL = "http://127.0.0.1:5000"


def mock_response(status_code, json_data):
    """Helper function to create a mock response object."""
    response = requests.models.Response()
    response.status_code = status_code
    response._content = json.dumps(json_data).encode("utf-8")
    return response


@pytest.fixture(scope="session", autouse=True)
def mock_requests():
    """Mock all requests to the API to prevent real HTTP calls."""
    with patch("requests.post") as mock_post, patch("requests.get") as mock_get, patch(
        "requests.put"
    ) as mock_put, patch("requests.delete") as mock_delete:

        def post_side_effect(url, **kwargs):
            _ = kwargs.get("json", {})
            if "/users" in url:
                return mock_response(201, {"message": "Registration successful!"})
            elif "/auth/token" in url:
                return mock_response(
                    200, {"message": "Login successful!", "token": "mock_token"}
                )
            elif "/cart/items" in url:
                return mock_response(200, {"message": "Item added to cart"})
            elif "/orders" in url:
                return mock_response(200, {"message": "Checkout successful"})
            return mock_response(400, {"error": "Invalid POST request"})

        def get_side_effect(url, **kwargs):
            if "/inventory" in url:
                return mock_response(200, {"results": []})
            elif "/cart" in url:
                return mock_response(200, {"cart": []})
            elif "/orders" in url:
                return mock_response(200, {"orders": []})
            elif "/order" in url:
                return mock_response(
                    200, {"order": {"order_id": "123", "status": "Processing"}}
                )
            return mock_response(404, {"error": "Not Found"})

        def put_side_effect(url, **kwargs):
            _ = kwargs.get("json", {})
            if "/orders/cancel" in url:
                return mock_response(200, {"message": "Order cancelled"})
            elif "/orders/status" in url:
                return mock_response(200, {"message": "Order status updated"})
            return mock_response(400, {"error": "Invalid PUT request"})

        def delete_side_effect(url, **kwargs):
            if "/cart/items" in url:
                return mock_response(200, {"message": "Item removed from cart"})
            return mock_response(400, {"error": "Invalid DELETE request"})

        mock_post.side_effect = post_side_effect
        mock_get.side_effect = get_side_effect
        mock_put.side_effect = put_side_effect
        mock_delete.side_effect = delete_side_effect

        yield  # Provide the mock context


def test_register_user():
    user_data = {
        "username": "new_user",
        "email": "new_user@example.com",
        "password": "newpassword",
        "address": "789 Test Ave",
    }
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    assert response.status_code == 201
    assert "Registration successful!" in response.json()["message"]


def test_login():
    login_data = {
        "email": "new_user@example.com",
        "password": "newpassword",
    }
    response = requests.post(f"{BASE_URL}/auth/token", json=login_data)
    assert response.status_code == 200
    assert "Login successful!" in response.json()["message"]
    assert "mock_token" == response.json()["token"]


def test_add_to_cart():
    item_data = {"name": "Office Chair", "quantity": 2}
    headers = {"Authorization": "Bearer mock_token"}
    response = requests.post(f"{BASE_URL}/cart/items", json=item_data, headers=headers)
    assert response.status_code == 200
    assert "Item added to cart" in response.json()["message"]


def test_remove_from_cart():
    remove_data = {"name": "Office Chair"}
    headers = {"Authorization": "Bearer mock_token"}
    response = requests.delete(
        f"{BASE_URL}/cart/items", json=remove_data, headers=headers
    )
    assert response.status_code == 200
    assert "Item removed from cart" in response.json()["message"]


def test_checkout():
    checkout_data = {"payment_info": "dummy_payment_info"}
    headers = {"Authorization": "Bearer mock_token"}
    response = requests.post(f"{BASE_URL}/orders", json=checkout_data, headers=headers)
    assert response.status_code == 200
    assert "Checkout successful" in response.json()["message"]


def test_get_order():
    headers = {"Authorization": "Bearer mock_token"}
    response = requests.get(f"{BASE_URL}/order/123", headers=headers)
    assert response.status_code == 200
    assert "order" in response.json()


def test_cancel_order():
    headers = {"Authorization": "Bearer mock_token"}
    response = requests.put(f"{BASE_URL}/orders/cancel", headers=headers)
    assert response.status_code == 200
    assert "Order cancelled" in response.json()["message"]


def test_update_order_status():
    status_data = {"status": "Shipped"}
    headers = {"Authorization": "Bearer mock_token"}
    response = requests.put(
        f"{BASE_URL}/orders/status", json=status_data, headers=headers
    )
    assert response.status_code == 200
    assert "Order status updated" in response.json()["message"]


if __name__ == "__main__":
    pytest.main()
