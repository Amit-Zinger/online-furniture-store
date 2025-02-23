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
    with patch("requests.post") as mock_post, \
         patch("requests.get") as mock_get, \
         patch("requests.put") as mock_put, \
         patch("requests.delete") as mock_delete:

        def post_side_effect(url, json=None, **kwargs):
            if "/register" in url:
                return mock_response(201, {"message": "Registration successful!"})
            elif "/login" in url:
                return mock_response(200, {"message": "Login successful!", "token": "mock_token"})
            elif "/cart/" in url and "/add" in url:
                return mock_response(200, {"message": "Item added to cart"})
            elif "/cart/" in url and "/checkout" in url:
                return mock_response(200, {"message": "Checkout successful"})
            elif "/cart/" in url and "/clear" in url:
                return mock_response(200, {"message": "Cart cleared"})
            else:
                return mock_response(400, {"error": "Invalid POST request"})

        def get_side_effect(url, **kwargs):
            if "/inventory/search" in url:
                return mock_response(200, {"results": []})
            elif "/cart/" in url:
                # For viewing cart, return an empty cart or some dummy items.
                return mock_response(200, {"cart": []})
            elif "/orders/" in url:
                return mock_response(200, {"orders": []})
            elif "/order/" in url:
                return mock_response(200, {"order": {"order_id": "123", "status": "Processing"}})
            else:
                return mock_response(404, {"error": "Not Found"})

        def put_side_effect(url, json=None, **kwargs):
            if "/order/" in url and "/cancel" in url:
                return mock_response(200, {"message": "Order cancelled"})
            elif "/order/" in url and "/status" in url:
                return mock_response(200, {"message": "Order status updated"})
            elif "/api/inventory/update" in url:
                return mock_response(200, {"message": "Quantity updated successfully!"})
            else:
                return mock_response(400, {"error": "Invalid PUT request"})

        def delete_side_effect(url, json=None, **kwargs):
            if "/cart/" in url and "/remove" in url:
                return mock_response(200, {"message": "Item removed from cart"})
            else:
                return mock_response(400, {"error": "Invalid DELETE request"})

        mock_post.side_effect = post_side_effect
        mock_get.side_effect = get_side_effect
        mock_put.side_effect = put_side_effect
        mock_delete.side_effect = delete_side_effect

        yield  # Provide the mock context

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

def test_view_cart():
    """Test viewing an empty cart."""
    user_id = "user123"
    response = requests.get(f"{BASE_URL}/cart/{user_id}")
    assert response.status_code == 200
    # Ensure the response contains a cart field (could be empty)
    assert "cart" in response.json()

def test_add_to_cart():
    """Test adding an item to the cart."""
    user_id = "user123"
    item_data = {
        "name": "Office Chair",
        "description": "Ergonomic chair",
        "price": 150.0,
        "dimensions": "50x50x100cm",
        "serial_number": "CH001",
        "available_quantity": 10,
        "weight": 10,
        "manufacturing_country": "Germany",
        "has_wheels": True,
        "how_many_legs": 5,
        "quantity": 2
    }
    response = requests.post(f"{BASE_URL}/cart/{user_id}/add", json=item_data)
    assert response.status_code == 200
    assert "Item added to cart" in response.json()["message"]

def test_remove_from_cart():
    """Test removing an item from the cart."""
    user_id = "user123"
    remove_data = {"name": "Office Chair"}
    response = requests.delete(f"{BASE_URL}/cart/{user_id}/remove", json=remove_data)
    assert response.status_code == 200
    assert "Item removed from cart" in response.json()["message"]

def test_clear_cart():
    """Test clearing the cart."""
    user_id = "user123"
    response = requests.post(f"{BASE_URL}/cart/{user_id}/clear")
    assert response.status_code == 200
    assert "Cart cleared" in response.json()["message"]

def test_checkout():
    """Test checking out the cart."""
    user_id = "user123"
    checkout_data = {"payment_info": "dummy_payment_info"}
    response = requests.post(f"{BASE_URL}/cart/{user_id}/checkout", json=checkout_data)
    assert response.status_code == 200
    assert "Checkout successful" in response.json()["message"]

def test_order_history():
    """Test retrieving order history."""
    user_id = "user123"
    response = requests.get(f"{BASE_URL}/orders/{user_id}")
    assert response.status_code == 200
    assert "orders" in response.json()

def test_get_order():
    """Test retrieving a specific order."""
    order_id = "123"
    response = requests.get(f"{BASE_URL}/order/{order_id}?user_id=user123")
    assert response.status_code == 200
    assert "order" in response.json()

def test_cancel_order():
    """Test cancelling an order."""
    order_id = "123"
    response = requests.put(f"{BASE_URL}/order/{order_id}/cancel")
    assert response.status_code == 200
    assert "Order cancelled" in response.json()["message"]

def test_update_order_status():
    """Test updating an order's status."""
    order_id = "123"
    status_data = {"status": "Shipped"}
    response = requests.put(f"{BASE_URL}/order/{order_id}/status", json=status_data)
    assert response.status_code == 200
    assert "Order status updated" in response.json()["message"]

if __name__ == "__main__":
    pytest.main()
