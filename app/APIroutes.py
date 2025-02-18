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
inventory = Inventory("data/inventory.pkl")  # Using pickle for inventory
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


app = Flask(__name__)

# ---------------------- Define API Functions ----------------------

def create_inventory_routes(app, inventory):
    """Attach API routes that interact with the given inventory instance."""

    @app.route("/inventory/search", methods=["GET"])
    def search_inventory():
        """
        Search for furniture items based on optional query parameters:
        - name: Search by furniture name
        - category: Search by furniture category (e.g., "Chair", "Table")
        - price_min & price_max: Search by price range
        """
        name = request.args.get("name")
        category = request.args.get("category")
        price_min = request.args.get("price_min", type=float)
        price_max = request.args.get("price_max", type=float)

        # Prepare the price range tuple if both min and max are provided
        price_range = (price_min, price_max) if price_min is not None and price_max is not None else None

        # Perform search in inventory
        results = inventory.search_by(name=name, category=category, price_range=price_range)

        if results:
            # Convert objects to dictionaries for JSON serialization
            results_data = [obj.__dict__ for obj in results]
            return jsonify({"results": results_data}), 200
        else:
            return jsonify({"message": "No matching items found"}), 404

    @app.route("/api/inventory", methods=["POST"])
    def add_inventory_item():
        """Add a new furniture item."""
        data = request.json
        if "type" not in data:
            return jsonify({"error": "Furniture type is required"}), 400

        success = inventory.add_item(data)
        if success:
            inventory.update_data()
            return jsonify({"message": "Item added successfully!"}), 201
        return jsonify({"error": "Failed to add item"}), 400

    @app.route("/api/inventory/update", methods=["PUT"])
    def update_inventory():
        """Update the quantity of an item."""
        data = request.json
        item = inventory.search_by(name=data["name"], category=data.get("type"))
        if not item:
            return jsonify({"error": "Item not found"}), 404

        inventory.update_quantity(item[0], data["quantity"])
        inventory.update_data()
        return jsonify({"message": "Quantity updated successfully!"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)

