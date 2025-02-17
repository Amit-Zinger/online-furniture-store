import json
import bcrypt
from abc import ABC, abstractmethod
from flask import Flask, request, jsonify, render_template
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)

app = Flask(__name__)
app.secret_key = "your_secret_key"

login_manager = LoginManager(app)
login_manager.login_view = "login"

USER_FILE = "users.json"


class User(UserMixin, ABC):
    def __init__(self, id, username, email, password, address, role="user"):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.address = address
        self.role = role

    def get_id(self):
        return str(self.id)

    @abstractmethod
    def get_role_specific_info(self):
        pass


class Client(User):
    def __init__(
            self,
            id,
            username,
            email,
            password,
            address,
            shop_cart=None,
            liked_list=None):
        super().__init__(id, username, email, password, address, role="client")
        self.shop_cart = shop_cart if shop_cart else []
        self.liked_list = liked_list if liked_list else []

    def add_cart(self, item):
        self.shop_cart.append(item)

    def like_product(self, product):
        if product not in self.liked_list:
            self.liked_list.append(product)

    def dislike_product(self, product):
        if product in self.liked_list:
            self.liked_list.remove(product)

    def edit_info(self, username=None, email=None, address=None, id=None):
        if username:
            self.username = username
        if email:
            self.email = email
        if address:
            self.address = address
        if id:
            self.id = id

        # Update the user in the JSON file
        users = get_all_users()
        for user in users:
            if user["id"] == self.id:
                user["username"] = self.username
                user["email"] = self.email
                user["address"] = self.address
                break

        with open(USER_FILE, "w") as file:
            json.dump(users, file, indent=4)

    def get_role_specific_info(self):
        return {"shop_cart": self.shop_cart, "liked_list": self.liked_list}


class Management(User):
    def __init__(
        self, id, username, email, password, address, worker_ID, role="manager"
    ):
        super().__init__(id, username, email, password, address, role=role)
        self.worker_ID = worker_ID

    def check_inventory(self):
        return "Checking inventory..."

    def check_low_inventory(self):
        return "Checking low inventory..."

    def get_role_specific_info(self):
        return {"worker_ID": self.worker_ID}


@login_manager.user_loader
def load_user(user_id):
    with open(USER_FILE, "r") as file:
        users = json.load(file)
    for user in users:
        if user["id"] == int(user_id):
            if user["role"] == "client":
                return Client(
                    user["id"],
                    user["username"],
                    user["email"],
                    user["password"],
                    user["address"],
                    user.get("shop_cart"),
                    user.get("liked_list"),
                )
            elif user["role"] == "manager":
                return Management(
                    user["id"],
                    user["username"],
                    user["email"],
                    user["password"],
                    user["address"],
                    user["worker_ID"],
                )
            else:
                return User(
                    user["id"],
                    user["username"],
                    user["email"],
                    user["password"],
                    user["address"],
                    user["role"],
                )
    return None


def get_all_users():
    with open(USER_FILE, "r") as file:
        return json.load(file)


def save_user(user):
    users = get_all_users()
    users.append(user)
    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        address = request.form["address"]
        role = request.form.get("role", "user")

        users = get_all_users()
        if any(user["username"] == username for user in users):
            return (
                jsonify({"msg": "Username already exists. Please choose another."}),
                400,
            )

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        new_user = {
            "id": max(user["id"] for user in users) + 1 if users else 1,
            "username": username,
            "email": email,
            "password": hashed_password,
            "address": address,
            "role": role,
        }

        if role == "client":
            new_user.update({"shop_cart": [], "liked_list": []})
        elif role == "manager":
            new_user.update(
                {
                    "worker_ID": max(
                        user.get("worker_ID", 0)
                        for user in users
                        if "worker_ID" in user
                    )
                    + 1
                }
            )

        save_user(new_user)
        return jsonify({"msg": "Registration successful! Please log in."}), 200


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = get_all_users()
        user = next((u for u in users if u["username"] == username), None)

        if user and bcrypt.checkpw(
            password.encode("utf-8"), user["password"].encode("utf-8")
        ):
            if user["role"] == "client":
                login_user(
                    Client(
                        user["id"],
                        user["username"],
                        user["email"],
                        user["password"],
                        user["address"],
                        user.get("shop_cart"),
                        user.get("liked_list"),
                    )
                )
            elif user["role"] == "manager":
                login_user(
                    Management(
                        user["id"],
                        user["username"],
                        user["email"],
                        user["password"],
                        user["address"],
                        user["worker_ID"],
                    )
                )
            else:
                login_user(
                    User(
                        user["id"],
                        user["username"],
                        user["email"],
                        user["password"],
                        user["address"],
                        user["role"],
                    )
                )
            return jsonify({"msg": "Login successful!"}), 200
        else:
            return jsonify({"msg": "Invalid username or password."}), 400


@app.route("/profile")
@login_required
def profile():
    base_info = {
        "username": current_user.username,
        "email": current_user.email,
        "address": current_user.address,
    }
    base_info.update(current_user.get_role_specific_info())
    return jsonify(base_info)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "Logged out successfully!"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
