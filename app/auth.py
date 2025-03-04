from flask import Flask, request, jsonify, session
from flask_login import LoginManager
from models.user import UserDB

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "super_secret_key"

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


def authenticate_user(email: str, password: str):
    """
    Authenticate a user by checking email and password.
    """
    user_db = UserDB.get_instance()
    user = next((u for u in user_db.user_data.values() if u.email == email), None)

    if user and user.verify_password(password):
        return user
    return None


def require_auth(func):
    """
    Decorator to enforce authentication via session.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Authentication required"}), 401
        return func(*args, **kwargs)
    return wrapper

# Authentication


def login():
    """
    User login using session-based authentication.
    """
    data = request.json
    user = authenticate_user(data["email"], data["password"])

    if user:
        session["user_id"] = user.user_id
        session["role"] = user.type
        session.permanent = True
        return jsonify({"message": "Login successful!"}), 200

    return jsonify({"error": "Invalid credentials"}), 401


def logout():
    """
    Logs out the user by clearing the session.
    """
    session.clear()
    return jsonify({"message": "User logged out successfully"}), 200
