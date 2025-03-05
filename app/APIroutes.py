from datetime import timedelta, datetime , timezone
from flask import Flask, request, jsonify, session, abort
from models.user import UserDB, Client, serialize_furniture
from models.inventory import Inventory
from models.order import OrderManager
from models.cart import PaymentGateway
from app.auth import require_auth,authenticate_user

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=2)



@app.before_request
def manage_session():
    session.permanent = True
    now = datetime.now(timezone.utc)

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
inventory = Inventory()
order_manager = OrderManager()
user_db = UserDB.get_instance()


def helper_updating_DB():
    inventory.update_data()
    order_manager.save_orders()
    user_db.save_users()

# ---------------------- User register ----------------------
@app.route("/users", methods=["POST"])
def register():
    data = request.json
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
    user = authenticate_user(data["email"], data["password"])
    if user:
        session["user_id"] = user.user_id
        session["role"] = user.type
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"error": "Invalid credentials"}), 401


# ---------------------- Cart Management ----------------------
@app.route("/cart/items", methods=["POST"])
@require_auth
def add_to_cart():
    data = request.json
    user = authenticate_user(data["email"], data["password"])
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    cart = user.shopping_cart

    item_name = data.get("name")
    quantity = int(data.get("quantity", 1))

    items = inventory.search_by(name=item_name)
    if not items or items[0].quantity <= quantity :
        return jsonify({"error": "Item not available or insufficient stock"}), 400

    # Check if item already exist in User ShoppingCart

    if items[0] in cart.items:
        count=0
        for i in cart.items:
            if items[0].name == i.name :
                count+=1
        if items[0].quantity <= quantity + count:
            return jsonify({"error": "Item insufficient stock"}), 400

    cart.add_item(items[0], quantity)
    return jsonify({"message": "Item added to cart"}), 200


@app.route("/cart/items", methods=["DELETE"])
@require_auth
def remove_from_cart():
    data = request.json
    user = authenticate_user(data["email"], data["password"])
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    cart = user.shopping_cart

    item_name = data.get("name")

    if (cart.remove_item(item_name)):
        return jsonify({"message": "Item removed from cart"}), 200
    else :
        return jsonify({"message": "Item not exist in user's cart"}), 400

# ---------------------- Checkout ----------------------
@app.route("/orders", methods=["POST"])
@require_auth
def checkout():
    data = request.json
    user = authenticate_user(data["email"], data["password"])
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    cart = user.shopping_cart

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
    user.shopping_cart.clear_cart()

    # Updating all DB after order made successfully
    helper_updating_DB()


    return jsonify({"message": "Checkout successful"}), 200


# ---------------------- Search Inventory ----------------------
@app.route("/inventory", methods=["GET"])
@require_auth
def search_product():
    data = request.json
    if not (authenticate_user(data["email"], data["password"])):
        return jsonify({"error": "Invalid credentials"}), 401

    name = data.get("name")
    category = data.get("category")
    min_price = data.get("min_price")
    max_price = data.get("max_price")

    results = inventory.search_by(
        name=name,
        category=category,
        price_range=(int(min_price), int(max_price)) if min_price is not None and max_price is not None else None
    )

    if not results:
        return jsonify({"message": "No products found"}), 404

    return jsonify([serialize_furniture(item) for item in results]), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
