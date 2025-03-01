import json
from datetime import datetime, timedelta

import bcrypt
import jwt
from flask import Flask, request, jsonify

from models.cart import ShoppingCart, PaymentGateway
from models.factory import FurnitureFactory
from models.furniture import Furniture
from models.inventory import Inventory
from models.order import OrderManager

app = Flask(__name__)
app.secret_key = "your_secret_key"
JWT_SECRET = "super_secret_jwt_key"
USER_FILE = "data/users.json"

# Initialize inventory and order manager
inventory = Inventory("data/inventory.pkl")  # Using pickle for inventory
order_manager = OrderManager()  # Singleton OrderManager instance

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

# ---------------------- Inventory Endpoints ----------------------


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
def update_inventory_route():
    """Update the quantity of an item."""
    data = request.json
    item = inventory.search_by(name=data["name"], category=data.get("type"))
    if not item:
        return jsonify({"error": "Item not found"}), 404

    inventory.update_quantity(item[0], data["quantity"])
    inventory.update_data()
    return jsonify({"message": "Quantity updated successfully!"}), 200

# ---------------------- Cart Endpoints ----------------------


# In-memory storage for active carts keyed by user_id.
active_carts = {}


def get_or_create_cart(user_id):
    if user_id not in active_carts:
        active_carts[user_id] = ShoppingCart(user_id)
    return active_carts[user_id]


@app.route('/cart/<user_id>', methods=['GET'])
def view_cart(user_id):
    """
    Returns the current contents of the shopping cart for a user.
    """
    cart = get_or_create_cart(user_id)
    items = []
    for entry in cart.get_cart():
        # Convert item objects to dictionaries for JSON serialization.
        item = entry["item"]
        item_data = item.__dict__.copy()
        item_data["quantity_in_cart"] = entry["quantity"]
        items.append(item_data)
    return jsonify({"cart": items}), 200


@app.route('/cart/<user_id>/add', methods=['POST'])
def add_to_cart(user_id):
    """
    Adds an item to the user's cart.
    Expected JSON body: { "name": "...", "description": "...", "price": <float>,
                           "dimensions": "...", "serial_number": "...", "available_quantity": <int>,
                           "weight": <int>, "manufacturing_country": "...",
                           "has_wheels": <bool>, "how_many_legs": <int>, "quantity": <int> }
    """
    data = request.json
    try:
        quantity = data.get("quantity", 1)
        # For this example, we assume the item is a Chair. In production, use a factory.
        from models.furniture import Chair  # Assuming Chair is a furniture class
        item = Chair(
            name=data["name"],
            description=data.get("description", ""),
            price=data.get("price", 100.0),
            dimensions=data.get("dimensions", "default"),
            serial_number=data.get("serial_number", "default"),
            quantity=data.get("available_quantity", 1),
            weight=data.get("weight", 1),
            manufacturing_country=data.get("manufacturing_country", "Unknown"),
            has_wheels=data.get("has_wheels", False),
            how_many_legs=data.get("how_many_legs", 4)
        )
        cart = get_or_create_cart(user_id)
        cart.add_item(item, quantity)
        return jsonify({"message": "Item added to cart"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/cart/<user_id>/remove', methods=['DELETE'])
def remove_from_cart(user_id):
    """
    Removes an item from the cart.
    Expected JSON body: { "name": "Item name" }
    """
    data = request.json
    cart = get_or_create_cart(user_id)
    cart.remove_item(data["name"])
    return jsonify({"message": "Item removed from cart"}), 200


@app.route('/cart/<user_id>/clear', methods=['POST'])
def clear_cart(user_id):
    """
    Clears the cart for a user.
    """
    cart = get_or_create_cart(user_id)
    cart.clear_cart()
    return jsonify({"message": "Cart cleared"}), 200


@app.route('/cart/<user_id>/checkout', methods=['POST'])
def checkout(user_id):
    """
    Initiates the checkout process.
    Expected JSON body: { "payment_info": "..." }
    """
    data = request.json
    cart = get_or_create_cart(user_id)
    payment_info = data.get("payment_info", "dummy_payment_info")
    payment_gateway = PaymentGateway()  # Payment always succeeds in our mock
    result = cart.purchase(payment_gateway, payment_info)
    if result:
        return jsonify({"message": "Checkout successful"}), 200
    else:
        return jsonify({"error": "Checkout failed"}), 400

# ---------------------- Order Endpoints ----------------------


@app.route('/orders/<user_id>', methods=['GET'])
def order_history(user_id):
    """
    Returns all orders for a specific user.
    """
    history = order_manager.get_order_history(user_id)
    return jsonify({"orders": history}), 200


@app.route('/order/<order_id>', methods=['GET'])
def get_order(order_id):
    """
    Retrieves details of a specific order.
    Expects a query parameter 'user_id' to ensure the order belongs to the requesting client.
    """
    user_id = request.args.get("user_id")
    order = order_manager.get_order(order_id, user_id)
    if order:
        return jsonify({"order": order}), 200
    else:
        return jsonify({"error": "Order not found"}), 404


@app.route('/order/<order_id>/cancel', methods=['PUT'])
def cancel_order(order_id):
    """
    Cancels an order by updating its status to 'Cancelled'.
    """
    order_manager.cancel_order(order_id)
    return jsonify({"message": "Order cancelled"}), 200


@app.route('/order/<order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """
    Updates the status of an order.
    Expected JSON body: { "status": "New Status" }
    """
    data = request.json
    new_status = data.get("status", "Processing")
    order_manager.update_order_status(order_id, new_status)
    return jsonify({"message": "Order status updated"}), 200


# ---------------------- Add new furniture type ----------------------


@app.route("/api/furniture/register", methods=["POST"])
def register_furniture():
    """Dynamically register a new type of furniture."""
    data = request.json
    name = data.get("name")
    attributes = data.get("attributes", {})

    if not name or not attributes:
        return jsonify({"error": "Missing furniture name or attributes"}), 400

    class CustomFurniture(Furniture):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

    FurnitureFactory.register_furniture(name, CustomFurniture)
    return jsonify({"message": f"{name} registered successfully!"}), 200


# ---------------------- Run the API ----------------------


if __name__ == "__main__":
    app.run(debug=True, port=5000)
