from datetime import datetime, timedelta
from flask import Flask, request, jsonify
import bcrypt
import jwt

from models.user import UserDB
from models.inventory import Inventory
from models.order import OrderManager
from models.cart import ShoppingCart, PaymentGateway
from auth import login_manager, require_auth, require_role

app = Flask(__name__)
app.secret_key = "your_secret_key"
JWT_SECRET = "super_secret_jwt_key"
USER_FILE = "data/users.json"

# Initialize inventory and order manager
inventory = Inventory("data/inventory.pkl")  # Using pickle for inventory
order_manager = OrderManager()  # Singleton OrderManager instance

# ---------------------- Helper Functions ----------------------

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
    """Register a new user."""
    data = request.json
    users = UserDB.get_all_users()
    if any(user["username"] == data["username"] for user in users):
        return jsonify({"error": "Username already exists"}), 400
    new_user = {
        "id": len(users) + 1,
        "username": data["username"],
        "email": data["email"],
        "password": bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
        "address": data["address"],
        "role": data.get("role", "client"),
    }
    users.append(new_user)
    UserDB.save_users(users)
    return jsonify({"message": "Registration successful!"}), 201

@app.route("/login", methods=["POST"])
def login():
    """User login."""
    data = request.json
    users = UserDB.get_all_users()
    user = next((u for u in users if u["username"] == data["username"]), None)
    if user and bcrypt.checkpw(data["password"].encode("utf-8"), user["password"].encode("utf-8")):
        token = jwt.encode({"user_id": user["id"], "role": user["role"], "exp": datetime.utcnow() + timedelta(hours=2)}, JWT_SECRET, algorithm="HS256")
        return jsonify({"message": "Login successful!", "token": token}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# ---------------------- Inventory Management ----------------------

@app.route("/inventory/search", methods=["GET"])
def search_inventory():
    """Search for furniture items based on optional query parameters."""
    name = request.args.get("name")
    category = request.args.get("category")
    price_min = request.args.get("price_min", type=float)
    price_max = request.args.get("price_max", type=float)
    price_range = (price_min, price_max) if price_min is not None and price_max is not None else None
    results = inventory.search_by(name=name, category=category, price_range=price_range)
    if results:
        results_data = [obj.__dict__ for obj in results]
        return jsonify({"results": results_data}), 200
    return jsonify({"message": "No matching items found"}), 404

@app.route("/api/inventory", methods=["POST"])
@require_auth
@require_role("manager")
def add_inventory_item(user_data):
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
@require_auth
@require_role("manager")
def update_inventory(user_data):
    """Update the quantity of an item."""
    data = request.json
    item = inventory.search_by(name=data["name"], category=data.get("type"))
    if not item:
        return jsonify({"error": "Item not found"}), 404
    inventory.update_quantity(item[0], data["quantity"])
    inventory.update_data()
    return jsonify({"message": "Quantity updated successfully!"}), 200

# ---------------------- Order Management ----------------------

@app.route("/cart/add", methods=["POST"])
@require_auth
def add_to_cart(user_data):
    """Adds an item to the user's shopping cart."""
    data = request.json
    user_id = user_data["user_id"]
    cart = ShoppingCart(user_id)
    item_name = data.get("name")
    quantity = data.get("quantity", 1)
    items = inventory.search_by(name=item_name)
    if not items or items[0].quantity < quantity:
        return jsonify({"error": "Item not available or insufficient stock"}), 400
    cart.add_item(items[0], quantity)
    return jsonify({"message": "Item added to cart"}), 200

@app.route("/cart/remove", methods=["DELETE"])
@require_auth
def remove_from_cart(user_data):
    """Removes an item from the user's shopping cart."""
    data = request.json
    user_id = user_data["user_id"]
    cart = ShoppingCart(user_id)
    item_name = data.get("name")
    cart.remove_item(item_name)
    return jsonify({"message": "Item removed from cart"}), 200

@app.route("/cart/checkout", methods=["POST"])
@require_auth
def checkout(user_data):
    """Processes checkout for the user's shopping cart."""
    user_id = user_data["user_id"]
    cart = ShoppingCart(user_id)
    if not cart.items:
        return jsonify({"error": "Cart is empty"}), 400
    total_price = cart.calculate_total()
    payment_info = request.json.get("payment_info")
    if not cart.validate_cart(inventory):
        return jsonify({"error": "Some items are out of stock"}), 400
    payment_gateway = PaymentGateway()
    if not payment_gateway.process_payment(total_price):
        return jsonify({"error": "Payment processing failed"}), 500
    order_manager.create_order(cart, payment_info, total_price)
    for item_dict in cart.items:
        item = item_dict["item"]
        inventory.update_quantity(item, item.quantity - item_dict["quantity"])
    cart.clear_cart()
    return jsonify({"message": "Checkout successful"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
