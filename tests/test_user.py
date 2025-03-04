import os
import pytest
import bcrypt
from typing import Generator
from models.user import User, Client, Management, UserDB

# Directory for test database
TEST_DB_FILE: str = "tests/test_users.json"


@pytest.fixture(scope="function")
def user_db() -> Generator[UserDB, None, None]:
    """Fixture to initialize and clean up the test database."""

    # Reset the singleton instance
    UserDB._instance = None  # Ensure a fresh instance is created
    db = UserDB.get_instance()  # Use the singleton method
    db.file_path = TEST_DB_FILE
    db.user_data = {}  # Clear existing data

    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)

    yield db

    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)


def test_hash_password() -> None:
    """Test password hashing and verification."""
    password: str = "TestPass123!"
    hashed_password: str = User.hash_password(password)
    assert bcrypt.checkpw(password.encode(), hashed_password.encode()), "Password hashing failed."


def test_verify_password() -> None:
    """Test password verification."""
    user: User = User(user_id="1", username="test_user", email="test@example.com",
                      password=User.hash_password("TestPass123!"), address="123 Main St")
    assert user.verify_password("TestPass123!"), "Password verification failed."
    assert not user.verify_password("WrongPass"), "Incorrect password should not pass verification."


def test_change_password(user_db: UserDB) -> None:
    """Test changing a user's password."""
    user: Client = Client(user_id="1", username="client1", email="client@example.com",
                          password=User.hash_password("OldPass123!"), address="123 Client St")
    user_db.add_user(user)
    user.change_password("NewPass456!")
    assert user.verify_password("NewPass456!"), "Password change failed."


def test_add_client(user_db: UserDB) -> None:
    """Test adding a client user to the database."""
    client: Client = Client(user_id="1", username="client1", email="client@example.com",
                            password=User.hash_password("ClientPass123!"), address="123 Client St")
    result: str = user_db.add_user(client)
    assert result == "User successfully added!", "Failed to add client."
    assert user_db.get_user(1) is not None, "User not found in database."


def test_edit_user(user_db: UserDB) -> None:
    """Test editing user information."""
    client: Client = Client(user_id="1", username="client1", email="client@example.com",
                            password=User.hash_password("ClientPass123!"), address="123 Client St")
    user_db.add_user(client)
    user_db.edit_user("1", username="new_client1", email="new_client@example.com", address="456 New St")
    updated_user = user_db.get_user(1)
    assert updated_user.username == "new_client1", "Username update failed."
    assert updated_user.email == "new_client@example.com", "Email update failed."
    assert updated_user.address == "456 New St", "Address update failed."


def test_delete_user(user_db: UserDB) -> None:
    """Test deleting a user from the database."""
    client: Client = Client(user_id="1", username="client1", email="client@example.com",
                            password=User.hash_password("ClientPass123!"), address="123 Client St")
    user_db.add_user(client)
    result: str = user_db.delete_user(1)
    assert result == "User successfully deleted.", "User deletion failed."
    assert user_db.get_user(1) is None, "User was not removed from database."


def test_edit_management_role(user_db: UserDB) -> None:
    """Test editing a management user's role."""
    manager: Management = Management(user_id="2", username="admin", email="admin@example.com",
                                     password=User.hash_password("AdminPass123!"), address="Admin St", rule="Manager")
    user_db.add_user(manager)
    manager.edit_rule("Director")
    assert manager.rule == "Director", "Manager role edit failed."


def test_authenticate_user(user_db: UserDB) -> None:
    """Test user authentication by email and password."""
    client: Client = Client(user_id="1", username="client1", email="client@example.com",
                            password=User.hash_password("ClientPass123!"), address="123 Client St")
    user_db.add_user(client)
    authenticated_user = user_db.authenticate_user("client@example.com", "ClientPass123!")
    assert authenticated_user is not None, "Authentication failed."
    assert authenticated_user.username == "client1", "Authenticated user data incorrect."

    failed_auth = user_db.authenticate_user("client@example.com", "WrongPass")
    assert failed_auth is None, "Authentication should fail with wrong password."


def test_user_uniqueness(user_db: UserDB) -> None:
    """Test that UserDB prevents duplicate user IDs."""
    client1: Client = Client(user_id="1", username="client1", email="client1@example.com",
                             password=User.hash_password("ClientPass123!"), address="123 Client St")
    client2: Client = Client(user_id="1", username="client2", email="client2@example.com",
                             password=User.hash_password("ClientPass456!"), address="456 Another St")
    user_db.add_user(client1)
    result: str = user_db.add_user(client2)
    assert result == "User ID already exists in UserDB", "Duplicate user ID was allowed!"


def test_invalid_password_hashing() -> None:
    """Test handling of incorrectly formatted password hashes."""
    invalid_user: User = User(user_id="1", username="invalid_user", email="invalid@example.com",
                              password="NotAHashedPassword", address="No Address")
    assert invalid_user.password.startswith("$2b$"), "Password hashing did not occur correctly."


def test_invalid_role_edit(user_db: UserDB) -> None:
    """Test attempting to edit a non-existent manager's role."""
    result: str = user_db.edit_user("999", rule="CEO")
    assert result == "User not found. Please check the ID and try again.", "Should not edit non-existent user."
