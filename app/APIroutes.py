from flask import Flask, request, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
import json
import os


###################################################### app
app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
###################################################### data

data_file = 'data.json'
if not os.path.exists(data_file):
    with open(data_file, 'w') as f:
        json.dump({"users": {}, "furniture": []}, f)


def load_data():
    pass


def save_data(data):
    pass


###################################################### classes

class Furniture:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def remove(self):
        pass

    def deduct_from_invetory(self, quantity):
        pass

    def to_dict(self):
        pass


class ShoppingCart:
    def __init__(self, user_id):
        self.user_id = user_id
        self.items = []

    def get_cart(self):
        pass

    def add_item(self, item, quantity):
        pass

    def clear_cart(self):
        pass

    def calculate_total(self):
        pass

    def purchase(self, payment_gateway):
        for item in self.items:
            if item.quantity > item.inventory:
                raise ValueError
            item.deduct_from_invetory(item.quanity)


class PaymentGateway:
    @staticmethod
    def process_payment(amount):
        pass


class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.cart = ShoppingCart(username)


###################################################### routes

@login_manager.user_loader
def load_user(user_id):
    data = load_data()
    users = data["users"]
    if user_id in users:
        return User(user_id)
    return None


@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    if not username:
        return jsonify({"error": "Username is required"}), 400

    data = load_data()
    if username in data["users"]:
        return jsonify({"error": "User already exists"}), 400

    data["users"][username] = {"shopping_cart": []}
    save_data(data)
    return jsonify({"message": f"User {username} registered successfully"})


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    if not username:
        return

    data = load_data()
    if username not in data["users"]:
        return

    user = User(username)
    login_user(user)


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()


@app.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    item_name = request.json.get('name')
    item_quantity = request.json.get('quantity')

    if not item_name:
        return

    ## simulates finding the item in the db
    item_params = load_data(furniture=item_name)

    item = Furniture(**item_params)

    current_user.cart.add_item(item, item_quantity)


@app.route('/purchase', methods=['POST'])
@login_required
def purchase():
    total_price = current_user.cart.calculate_total()
    if total_price == 0:
        return

    payment_gateway = PaymentGateway()

    if current_user.cart.purchase(payment_gateway):
        current_user.cart.clear_cart()


@app.route('/cart', methods=['GET'])
@login_required
def view_cart():
    cart = current_user.cart.get_cart()
    total_price = current_user.cart.calculate_total()
    return jsonify({"items": cart, "total_price": total_price})


if __name__ == '__main__':
    app.run(debug=True)
