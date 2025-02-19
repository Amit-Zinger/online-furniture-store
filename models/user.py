import json
import os
from abc import ABC, abstractmethod
import bcrypt

USER_FILE = "users.json"  # JSON file as a database


class User(ABC):
    users_list = {}  # Dictionary {id: user_object}

    def __init__(self, id, username, email, password, address, role="user"):
        self.id = id
        self.username = username
        self.email = email
        self.password = self.hash_password(password) if not password.startswith("$2b$") else password
        self.address = address
        self.role = role
        User.users_list[self.id] = self  # Add to users dictionary
        save_users()  # Save to file

    def hash_password(self, password):
        """Hashes the password using bcrypt."""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, password):
        """Verifies a hashed password."""
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    def get_id(self):
        return str(self.id)

    @abstractmethod
    def get_role_specific_info(self):
        pass

    @abstractmethod
    def get_user_type(self):
        pass


class Client(User):
    def __init__(self, id, username, email, password, address, shop_cart=None, liked_list=None):
        super().__init__(id, username, email, password, address, role="client")
        self.shop_cart = shop_cart if shop_cart else []
        self.liked_list = liked_list if liked_list else []
        self.order_history = []

    def add_cart(self, item):
        self.shop_cart.append(item)
        save_users()

    def like_product(self, product):
        if product not in self.liked_list:
            self.liked_list.append(product)
            save_users()

    def dislike_product(self, product):
        if product in self.liked_list:
            self.liked_list.remove(product)
            save_users()

    def edit_info(self, username=None, email=None, address=None):
        if username:
            self.username = username
        if email:
            self.email = email
        if address:
            self.address = address

        # Update user dictionary and save
        User.users_list[self.id] = self
        save_users()

    def get_role_specific_info(self):
        return {
            "shop_cart": self.shop_cart,
            "liked_list": self.liked_list,
            "order_history": self.order_history,
        }

    def get_user_type(self):
        return "Client"


class Management(User):
    def __init__(self, id, username, email, password, address):
        super().__init__(id, username, email, password, address, role="manager")

    def check_inventory(self):
        return "Checking inventory..."

    def check_low_inventory(self):
        return "Checking low inventory..."

    def get_role_specific_info(self):
        return {}  # No additional fields for management

    def get_user_type(self):
        return "Management"


# -------- JSON File Handling -------- #
def get_all_users():
    """Loads all users from the JSON file into the users_list dictionary."""
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as file:
            json.dump({}, file, indent=4)  # Create an empty JSON object

    with open(USER_FILE, "r") as file:
        data = json.load(file)

    User.users_list = {
        int(id): (Client(**user) if user["role"] == "client" else Management(**user))
        for id, user in data.items()
    }
    return User.users_list


def save_users():
    """Saves all users from the dictionary to the JSON file."""
    with open(USER_FILE, "w") as file:
        json.dump(
            {id: user.__dict__ for id, user in User.users_list.items()}, file, indent=4
        )


# Load users when script starts
get_all_users()
