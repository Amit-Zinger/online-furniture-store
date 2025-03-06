from functools import wraps
from flask import session, jsonify
from typing import Callable
from models.user import UserDB

def authenticate_user(username: str, password: str)-> UserDB:
    """
    Authenticate a user by checking email and password.
    """
    user_db = UserDB.get_instance()
    user = next((u for u in user_db.user_data.values() if u.username == username), None)

    if user and user.verify_password(password):
        return user
    return None


def require_auth(func: Callable):
    """
    Decorator to enforce authentication via session.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Authentication required"}), 401
        return func(*args, **kwargs)
    return wrapper


def require_role(required_role: str):
    """
    Decorator to enforce role-based access control.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "role" not in session or session["role"] != required_role:
                return jsonify({"error": "Unauthorized"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator
