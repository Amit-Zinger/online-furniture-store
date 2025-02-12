import requests

BASE_URL = "http://127.0.0.1:5000"

def test_order_process():
    """Regression Test - Ensures order affects all components correctly."""
    # 1️⃣ Create user & login
    user_data = {"username": "regression_test", "password": "testpass"}
    requests.post(f"{BASE_URL}/register", json=user_data)
    login_res = requests.post(f"{BASE_URL}/login", json=user_data)
    token = login_res.json().get("token")

    # 2️⃣ Add item to cart
    headers = {"Authorization": token}
    requests.post(f"{BASE_URL}/cart/add", json={"item": {"name": "Chair", "quantity": 1}}, headers=headers)

    # 3️⃣ Checkout
    checkout_res = requests.post(f"{BASE_URL}/checkout", headers=headers)
    assert checkout_res.status_code == 200

    # 4️⃣ Check inventory is updated
    inventory_res = requests.get(f"{BASE_URL}/inventory")
    assert "Chair" not in inventory_res.json()  # Ensure item was removed from inventory
