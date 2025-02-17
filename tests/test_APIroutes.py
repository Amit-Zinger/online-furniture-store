import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"  # URL של ה- Flask API


@pytest.fixture
def test_user():
    """רושם משתמש חדש לבדיקה"""
    user_data = {
        "username": "test_user",
        "email": "test_user@example.com",
        "password": "test1234",
        "address": "123 Test Street",
        "role": "client",
    }
    response = requests.post(f"{BASE_URL}/register", json=user_data)
    return user_data  # מחזיר את הנתונים שנשלחו


@pytest.fixture
def test_manager():
    """רושם משתמש מנהל לבדיקה"""
    manager_data = {
        "username": "test_manager",
        "email": "manager@example.com",
        "password": "admin1234",
        "address": "456 Admin St",
        "role": "manager",
    }
    response = requests.post(f"{BASE_URL}/register", json=manager_data)
    return manager_data  # מחזיר את הנתונים שנשלחו


@pytest.fixture
def auth_token(test_user):
    """מבצע התחברות ומחזיר טוקן"""
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]}
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    return response.json().get("token")


@pytest.fixture
def manager_token(test_manager):
    """מבצע התחברות ומחזיר טוקן של מנהל"""
    login_data = {
        "username": test_manager["username"],
        "password": test_manager["password"],
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    return response.json().get("token")


def test_register_user():
    """בדיקת רישום משתמש חדש"""
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


def test_login(auth_token):
    """בדיקת התחברות תקינה"""
    assert auth_token is not None


def test_add_inventory_item(manager_token):
    """בדיקת הוספת פריט למלאי (דורש הרשאת מנהל)"""
    headers = {"Authorization": manager_token}
    item_data = {
        "type": "Chair",
        "name": "Office Chair",
        "description": "Ergonomic chair with wheels",
        "price": 120.0,
        "dimensions": "60x60x120 cm",
        "serial_number": "CH001",
        "quantity": 10,
        "weight": 15.5,
        "manufacturing_country": "Germany",
        "has_wheels": True,
        "how_many_legs": 5,
    }
    response = requests.post(
        f"{BASE_URL}/inventory/add", json=item_data, headers=headers
    )
    assert response.status_code == 201
    assert "Item added successfully!" in response.json()["message"]


def test_add_to_cart(auth_token):
    """בדיקת הוספת פריט לעגלת הקניות"""
    headers = {"Authorization": auth_token}
    cart_item = {"item": {"name": "Office Chair", "quantity": 1}}
    response = requests.post(
        f"{BASE_URL}/cart/add",
        json=cart_item,
        headers=headers)
    assert response.status_code == 200
    assert "Item added to cart" in response.json()["message"]


def test_checkout(auth_token):
    """בדיקת תהליך קנייה"""
    headers = {"Authorization": auth_token}
    response = requests.post(f"{BASE_URL}/checkout", headers=headers)
    assert response.status_code == 200
    assert "Order placed successfully!" in response.json()["message"]
