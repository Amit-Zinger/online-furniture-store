from datetime import datetime, timedelta
from flask import Flask, request, jsonify
import jwt
from flask_login import logout_user
from models.user import UserDB, Client, serialize_furniture
from models.inventory import Inventory
from models.order import OrderManager
from models.cart import ShoppingCart, PaymentGateway
from app.auth import require_auth

app = Flask(__name__)
app.secret_key = "your_secret_key"
JWT_SECRET = "super_secret_jwt_key"
USER_FILE = "data/users.json"

# ----------------- Initialize inventory and OrderManager -----------------
inventory = Inventory("data/inventory.pkl")  # Using pickle for inventory
order_manager = OrderManager()  # Singleton OrderManager instance


# ---------------------- User register ----------------------
@app.route("app/auth/register", methods=["POST"])
def register():
    """
    Register a new user.
    """
    data = request.json
    user_db = UserDB()
    if any(u.email == data["email"] for u in user_db.user_data.values()):
        return jsonify({"error": "Email already registered"}), 400
    new_user = Client(
        user_id=len(user_db.user_data) + 1,
        username=data["username"],
        email=data["email"],
        password=data["password"],
        address=data["address"]
    )
    user_db.add_user(new_user)
    return jsonify({"message": "Registration successful!"}), 201


# ---------------------- User Login and Logout ----------------------
@app.route("app/auth/login", methods=["POST"])
def login():
    """
    User login.
    """
    data = request.json
    user_db = UserDB()
    user = user_db.authenticate_user(data["email"], data["password"])
    if user:
        token = jwt.encode({"user_id": user.user_id, "role": user.type,
                            "exp": datetime.utcnow() + timedelta(hours=2)}, JWT_SECRET, algorithm="HS256")
        return jsonify({"message": "Login successful!", "token": token}), 200
    return jsonify({"error": "Invalid credentials"}), 401


@app.route("app/auth/logout", methods=["POST"])
@require_auth
def logout(user_data):
    """
    Logout the current user.
    """
    user_id = user_data["user_id"]
    logout_user()
    return jsonify({"message": f"User {user_id} logged out successfully"}), 200


# ---------------------- add or remove from cart ----------------------
@app.route("model/cart/add", methods=["POST"])
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


@app.route("model/cart/remove", methods=["DELETE"])
@require_auth
def remove_from_cart(user_data):
    """Removes an item from the user's shopping cart."""
    data = request.json
    user_id = user_data["user_id"]
    cart = ShoppingCart(user_id)

    item_name = data.get("name")
    cart.remove_item(item_name)
    return jsonify({"message": "Item removed from cart"}), 200


# ---------------------- checkout ----------------------
@app.route("/cart/checkout", methods=["POST"])
@require_auth
def checkout(user_data):
    """Processes checkout for the user's shopping cart."""
    user_id = user_data["user_id"]
    cart = ShoppingCart(user_id)

    if not cart.items:
        return jsonify({"error": "Cart is empty"}), 400

    # Validate inventory availability
    if not cart.validate_cart(inventory):
        return jsonify({"error": "Some items are out of stock"}), 400

    total_price = cart.calculate_total()
    if total_price is None:
        return jsonify({"error": "Failed to calculate total price"}), 500

    payment_info = request.json.get("payment_info")

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


# ---------------------- search product ----------------------
@app.route("model/inventory/search", methods=["GET"])
def search_product():
    """Search for products by name, category, or price range, returning all relevant attributes."""
    name = request.args.get("name")
    category = request.args.get("category")
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)

    # search by name category or price 
    results = inventory.search_by(
        name=name,
        category=category,
        price_range=(min_price, max_price) if min_price is not None and max_price is not None else None
    )

    # no match found
    if not results:
        return jsonify({"message": "No products found"}), 404

    return jsonify([serialize_furniture(item) for item in results]), 200
# ---------------------- Run the API ----------------------


if __name__ == "__main__":
    app.run(debug=True, port=5000)
