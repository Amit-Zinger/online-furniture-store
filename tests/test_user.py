import pytest
import os
import bcrypt
from models.user import Client, Management, UserDB, USER_FILE
from models.cart import ShoppingCart


@pytest.fixture(scope="function")
def setup_user_db():
    """Setup test database and ensure a clean JSON file for each test"""
    if os.path.exists(USER_FILE):
        os.remove(USER_FILE)  # Ensure a fresh start

    db = UserDB()  # Initialize a new user database

    client = Client(id=1, username="test_client", email="client@test.com", password="password123", address="123 Street")
    manager = Management(id=2, username="test_manager", email="manager@test.com", password="password123",
                         address="456 Avenue", rule="admin")

    db.add_user(client)
    db.add_user(manager)

    return db  # Return the test database instance


def test_user_creation(setup_user_db):
    db = setup_user_db
    client = db.get_user(1)
    manager = db.get_user(2)

    assert client.get_user_type() == "Client"
    assert manager.get_user_type() == "Management"
    assert client.verify_password("password123")
    assert manager.verify_password("password123")


def test_edit_client_info(setup_user_db):
    db = setup_user_db
    db.edit_user(1, username="new_client", email="new_client@test.com", address="789 Boulevard")

    client = db.get_user(1)
    assert client.username == "new_client"
    assert client.email == "new_client@test.com"
    assert client.address == "789 Boulevard"


def test_edit_manager_info(setup_user_db):
    db = setup_user_db
    db.edit_user(2, username="new_manager", email="new_manager@test.com", address="999 Street", rule="superadmin")

    manager = db.get_user(2)
    assert manager.username == "new_manager"
    assert manager.email == "new_manager@test.com"
    assert manager.address == "999 Street"
    assert manager.rule == "superadmin"


def test_password_verification(setup_user_db):
    db = setup_user_db
    client = db.get_user(1)

    assert client.verify_password("password123")
    assert not client.verify_password("wrongpassword")


def test_password_is_hashed(setup_user_db):
    db = setup_user_db
    client = db.get_user(1)

    assert client.password.startswith("$2b$")  # bcrypt hashed passwords start with $2b$
    assert bcrypt.checkpw("password123".encode("utf-8"), client.password.encode("utf-8"))


def test_save_and_load_users(setup_user_db):
    """Test that users are correctly saved and loaded from the JSON file."""
    db = UserDB()  # Reload from file
    assert len(db.get_all_users()) == 2  # Ensure users were loaded correctly

    client = db.get_user(1)
    manager = db.get_user(2)

    assert client.username == "test_client"
    assert manager.username == "test_manager"


def test_client_shopping_cart_creation(setup_user_db):
    db = setup_user_db
    client = db.get_user(1)

    assert isinstance(client.shopping_cart, ShoppingCart)
    assert client.shopping_cart.user_id == client.id





def test_authenticate_user(setup_user_db):
    db = setup_user_db
    user = db.authenticate_user("client@test.com", "password123")

    assert user is not None
    assert user.username == "test_client"

    wrong_user = db.authenticate_user("client@test.com", "wrongpassword")
    assert wrong_user is None  # Should fail authentication

    non_existent_user = db.authenticate_user("nonexistent@test.com", "password123")
    assert non_existent_user is None  # Should fail authentication
