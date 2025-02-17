from flask import Flask, request, jsonify
import jwt
from datetime import datetime, timedelta
import bcrypt
import json
import os
from models.user import Client, Management
from models.cart import ShoppingCart
from models.inventory import Inventory
from models.order import OrderManager

app = Flask(__name__)
app.secret_key = "your_secret_key"
JWT_SECRET = "super_secret_jwt_key"
USER_FILE = "data/users.json"

# Initialize inventory and orders
inventory = Inventory("data/inventory.pkl")
orders = []


# ---------------------- Helper Functions ----------------------


def get_all_users():
    """Load all users from JSON file."""
    try:
        with open(USER_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_users(users):
    """Save updated user list to JSON file."""
    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)


def authenticate(token):
    """Authenticate a user via JWT token."""
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


# ---------------------- User Management ----------------------


@app.route("/register", methods=["POST"])
def register():
    """Register a new user (Client or Manager)."""
    data = request.json
    users = get_all_users()

    if any(user["username"] == data["username"] for user in users):
        return jsonify({"error": "Username already exists"}), 400

    new_user = {
        "id": len(users) + 1,
        "username": data["username"],
        "email": data["email"],
        "password": bcrypt.hashpw(
            data["password"].encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8"),
        "address": data["address"],
        "role": data.get("role", "client"),
    }
    if new_user["role"] == "client":
        new_user.update({"shop_cart": [], "liked_list": []})
    elif new_user["role"] == "manager":
        new_user.update(
            {"worker_ID": len([u for u in users if u.get("worker_ID")]) + 1}
        )

    users.append(new_user)
    save_users(users)
    return jsonify({"message": "Registration successful!"}), 201


@app.route("/login", methods=["POST"])
def login():
    """User login."""
    data = request.json
    users = get_all_users()
    user = next((u for u in users if u["username"] == data["username"]), None)

    if user and bcrypt.checkpw(
        data["password"].encode("utf-8"), user["password"].encode("utf-8")
    ):
        token = jwt.encode(
            {
                "user_id": user["id"],
                "role": user["role"],
                "exp": datetime.utcnow() + timedelta(hours=2),
            },
            JWT_SECRET,
            algorithm="HS256",
        )
        return jsonify({"message": "Login successful!", "token": token}), 200
    return jsonify({"error": "Invalid credentials"}), 401


# ---------------------- Inventory Management ----------------------


@app.route("/inventory", methods=["GET"])
def get_inventory():
    """Get all available furniture in inventory."""
    return jsonify(inventory.data.to_dict()), 200


@app.route("/inventory/add", methods=["POST"])
def add_inventory_item():
    """Add a new furniture item to inventory (Admin only)."""
    token = request.headers.get("Authorization")
    user_data = authenticate(token)

    if not user_data or user_data["role"] != "manager":
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    inventory.add_item(data)
    inventory.update_data()
    return jsonify({"message": "Item added successfully!"}), 201


@app.route("/inventory/remove", methods=["DELETE"])
def remove_inventory_item():
    """Remove furniture item from inventory (Admin only)."""
    token = request.headers.get("Authorization")
    user_data = authenticate(token)

    if not user_data or user_data["role"] != "manager":
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    if inventory.remove_item(furniture_desc=data):
        inventory.update_data()
        return jsonify({"message": "Item removed successfully!"}), 200
    return jsonify({"error": "Item not found"}), 404


# ---------------------- Shopping Cart ----------------------


@app.route("/cart", methods=["GET"])
def view_cart():
    """View shopping cart contents."""
    token = request.headers.get("Authorization")
    user_data = authenticate(token)

    if not user_data:
        return jsonify({"error": "Unauthorized"}), 401

    users = get_all_users()
    user = next((u for u in users if u["id"] == user_data["user_id"]), None)

    if user:
        return jsonify({"cart": user["shop_cart"]}), 200
    return jsonify({"error": "User not found"}), 404


@app.route("/cart/add", methods=["POST"])
def add_to_cart():
    """Add furniture to shopping cart."""
    token = request.headers.get("Authorization")
    user_data = authenticate(token)

    if not user_data:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    users = get_all_users()
    user = next((u for u in users if u["id"] == user_data["user_id"]), None)

    if user:
        user["shop_cart"].append(data["item"])
        save_users(users)
        return jsonify({"message": "Item added to cart"}), 200
    return jsonify({"error": "User not found"}), 404


# ---------------------- Checkout Process ----------------------


@app.route("/checkout", methods=["POST"])
def checkout():
    """Process user checkout and finalize the order."""
    token = request.headers.get("Authorization")
    user_data = authenticate(token)

    if not user_data:
        return jsonify({"error": "Unauthorized"}), 401

    users = get_all_users()
    user = next((u for u in users if u["id"] == user_data["user_id"]), None)

    if user and user["shop_cart"]:
        orders.append(OrderManager())
        user["shop_cart"] = []
        save_users(users)
        return jsonify({"message": "Order placed successfully!"}), 200
    return jsonify({"error": "Cart is empty or user not found"}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)
