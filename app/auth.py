from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, logout_user
import jwt
from datetime import datetime, timedelta
from functools import wraps
from models.user import UserDB, Client, Management

# Secret keys for JWT
JWT_SECRET = "super_secret_jwt_key"

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app()


def authenticate(token: str):
    """
    Decode and verify a JWT token.
    """
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def require_auth(func):
    """
    Decorator to enforce authentication via JWT.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Authentication required"}), 401
        user_data = authenticate(token)
        if not user_data:
            return jsonify({"error": "Invalid or expired token"}), 401
        return func(user_data, *args, **kwargs)
    return wrapper


def require_role(required_role: str):
    """
    Decorator to enforce role-based access control.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(user_data, *args, **kwargs):
            if user_data.get("role") != required_role:
                return jsonify({"error": "Unauthorized"}), 403
            return func(user_data, *args, **kwargs)
        return wrapper
    return decorator
