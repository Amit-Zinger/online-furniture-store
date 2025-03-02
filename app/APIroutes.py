from datetime import datetime, timedelta
from models.user import UserDB
import bcrypt
import jwt
from flask import Flask
from flask import request, jsonify
from models.inventory import Inventory
from models.order import OrderManager
from auth import login_manager
from flask import Flask, request, jsonify
from models.inventory import Inventory
from models.cart import ShoppingCart, PaymentGateway
from models.order import OrderManager


app = Flask(__name__)
app.secret_key = "your_secret_key"
JWT_SECRET = "super_secret_jwt_key"
USER_FILE = "data/users.json"

app = Flask(__name__)
# Initialize inventory and order manager
inventory = Inventory("data/inventory.pkl")
order_manager = OrderManager()
# ---------------------- Helper Functions ----------------------

def authenticate(token):
    """Authenticate a user via JWT token."""
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def require_auth(func):
    """Decorator to ensure authentication via JWT."""
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        user_data = authenticate(token)
        if not user_data:
            return jsonify({"error": "Authentication required"}), 401
        return func(user_data, *args, **kwargs)
    return wrapper


def require_role(required_role):
    """Decorator to enforce role-based access control."""
    def decorator(func):
        def wrapper(user_data, *args, **kwargs):
            if user_data["role"] != required_role:
                return jsonify({"error": "Unauthorized"}), 403
            return func(user_data, *args, **kwargs)
        return wrapper
    return decorator

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


@app.route("/api/inventory/update", methods=["PUT"])
@require_auth
@require_role("manager")
def update_inventory_route(user_data):
    """Update the quantity of an item (only managers)."""
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

    # Check item availability
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

    # Validate inventory availability
    if not cart.validate_cart(inventory):
        return jsonify({"error": "Some items are out of stock"}), 400

    # Process payment
    payment_gateway = PaymentGateway()
    if not payment_gateway.process_payment(total_price):
        return jsonify({"error": "Payment processing failed"}), 500

    # Create order
    order_manager.create_order(cart, payment_info, total_price)

    # Update inventory
    for item_dict in cart.items:
        item = item_dict["item"]
        new_quantity = item.quantity - item_dict["quantity"]
        inventory.update_quantity(item, new_quantity)

    cart.clear_cart()
    return jsonify({"message": "Checkout successful"}), 200


# ---------------------- Run the API ----------------------


if __name__ == "__main__":
    app.run(debug=True, port=5000)
