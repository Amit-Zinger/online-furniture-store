from datetime import timedelta, datetime
from flask import Flask, request, jsonify, session, abort
from models.user import UserDB, Client, serialize_furniture
from models.inventory import Inventory
from models.order import OrderManager
from models.cart import ShoppingCart, PaymentGateway
from app.auth import require_auth

app = Flask(__name__)
app.secret_key = "your_secret_key"
USER_FILE = "data/users.json"


app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=2)


@app.before_request
def manage_session():
    session.permanent = True
    now = datetime.utcnow()

    # If the user is logged in, check if the session expiration time has passed
    if "user_id" in session:
        if "last_activity" in session:
            last_activity = session["last_activity"]
            inactivity_period = now - last_activity

            if inactivity_period > app.config["PERMANENT_SESSION_LIFETIME"]:
                session.clear()  # Clear session if expired
                abort(401)

        # Update last activity time
        session["last_activity"] = now


# Initialize inventory and OrderManager
inventory = Inventory("data/inventory.pkl")  # Using pickle for inventory
order_manager = OrderManager()  # Singleton OrderManager instance


# ---------------------- User register ----------------------
@app.route("/users", methods=["POST"])
def register():
    data = request.json
    user_db = UserDB.get_instance()
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


# ---------------------- User Login ----------------------
@app.route("/auth/login", methods=["POST"])
def login():
    data = request.json
    user_db = UserDB.get_instance()
    user = user_db.authenticate_user(data["email"], data["password"])
    if user:
        session["user_id"] = user.user_id
        session["role"] = user.type
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"error": "Invalid credentials"}), 401


# ---------------------- Cart Management ----------------------
@app.route("/cart/items", methods=["POST"])
@require_auth
def add_to_cart(user_data):
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


@app.route("/cart/items", methods=["DELETE"])
@require_auth
def remove_from_cart(user_data):
    data = request.json
    user_id = user_data["user_id"]
    cart = ShoppingCart(user_id)

    item_name = data.get("name")
    cart.remove_item(item_name)
    return jsonify({"message": "Item removed from cart"}), 200


# ---------------------- Checkout ----------------------
@app.route("/orders", methods=["POST"])
@require_auth
def checkout(user_data):
    user_id = user_data["user_id"]
    cart = ShoppingCart(user_id)

    if not cart.items:
        return jsonify({"error": "Cart is empty"}), 400

    if not cart.validate_cart(inventory):
        return jsonify({"error": "Some items are out of stock"}), 400

    total_price = cart.calculate_total()
    if total_price is None:
        return jsonify({"error": "Failed to calculate total price"}), 500

    payment_info = request.json.get("payment_info")
    payment_gateway = PaymentGateway()
    if not payment_gateway.process_payment(payment_info, total_price):
        return jsonify({"error": "Payment processing failed"}), 500

    order_manager.create_order(cart, payment_info, total_price)
    for item in cart.items:
        inventory.update_quantity(item, item.quantity - 1)

    cart.clear_cart()
    return jsonify({"message": "Checkout successful"}), 200


# ---------------------- Search Inventory ----------------------
@app.route("/inventory", methods=["GET"])
def search_product():
    name = request.args.get("name")
    category = request.args.get("category")
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)

    results = inventory.search_by(
        name=name,
        category=category,
        price_range=(min_price, max_price) if min_price is not None and max_price is not None else None
    )

    if not results:
        return jsonify({"message": "No products found"}), 404

    return jsonify([serialize_furniture(item) for item in results]), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
