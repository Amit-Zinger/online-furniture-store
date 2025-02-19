import json
import os
from abc import ABC, abstractmethod
import bcrypt
from models.cart import ShoppingCart
from models.order import OrderManager

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
    def __init__(self, id, username, email, password, address):
        super().__init__(id, username, email, password, address, role="client")
        self.shopping_cart = ShoppingCart(id)
        self.liked_list = []
        self.order_history = OrderManager.get_order_history(id)



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
            "shop_cart": self.shopping_cart,
            "order_history": self.order_history,
        }

    def get_user_type(self):
        return "Client"




class Management(User):
    def __init__(self, id, username, email, password, address):
        super().__init__(id, username, email, password, address, role="manager")

    def check_low_inventory(self, inventory):

        low_furniture_list = []
        category_types_list = [
            "Chair",
            "Sofa",
            "Table",
            "Bed",
            "Closet"]

        for catagory in category_types_list:
            # Reciving all furniture object for specific catagory from inventory database
            atr_list = inventory.search_by(catagory=catagory)
            # Search for furniture with quantity 0
            for atr in atr_list:
                if (atr.quantity == 0):
                    low_furniture_list.append(atr)

        return low_furniture_list


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
