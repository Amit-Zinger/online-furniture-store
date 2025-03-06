import pytest

from app.auth import authenticate_user
from models.user import UserDB, Client, Management


@pytest.fixture(scope="module")
def setup_user_db() -> UserDB:
    """
    Create a shared test user database for all tests without modifying the original database.
    """
    user_db = UserDB.get_instance()
    user_db.user_data = {}  # Start with a clean database
    client_user = Client(
        user_id="1",
        username="client_user",
        email="client@example.com",
        password="ClientPass123!",
        address="123 Client St"
    )
    manager_user = Management(
        user_id="2",
        username="manager_user",
        email="manager@example.com",
        password="ManagerPass123!",
        address="456 Manager St",
        role="Admin"
    )
    user_db.add_user(client_user)
    user_db.add_user(manager_user)
    return user_db


def test_authenticate_valid_user(setup_user_db: UserDB) -> None:
    """
    Test that a user with valid credentials can authenticate successfully.
    """
    user = authenticate_user("client_user", "ClientPass123!")
    assert user is not None, "User should be authenticated successfully"
    assert user.email == "client@example.com"


def test_authenticate_invalid_password(setup_user_db: UserDB) -> None:
    """
    Test authentication fails for a wrong password.
    """
    user = authenticate_user("client_user", "WrongPassword")
    assert user is None, "Authentication should fail with an incorrect password"


def test_authenticate_non_existent_user(setup_user_db: UserDB) -> None:
    """
    Test authentication fails for a non-existent user.
    """
    user = authenticate_user("client_user", "SomePassword")
    assert user is None, "Authentication should fail for an email not in the database"
