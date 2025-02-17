import pytest
import requests
import subprocess
import time

BASE_URL = "http://127.0.0.1:5000"

@pytest.fixture(scope="session", autouse=True)
def setup_flask_server():
    """Start the Flask API before running tests."""
    server = subprocess.Popen(["python", "APIroutes.py"])
    time.sleep(5)  # Wait for the server to start
    yield
    server.terminate()  # Stop the server after tests

def test_register_user():
    """Test new user registration."""
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
    """Test valid user login."""
    login_data = {
        "username": "new_user",
        "password": "newpassword",
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    assert response.status_code == 200
    assert "Login successful!" in response.json()["message"]

if __name__ == "__main__":
    pytest.main()
