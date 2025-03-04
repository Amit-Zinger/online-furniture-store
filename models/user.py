import json
import os
import sys
import bcrypt
from abc import ABC
from typing import Dict, Optional
from models.cart import ShoppingCart
from models.furniture import Furniture
from models.factory import FurnitureFactory

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# -------- Helper Func -------- #
def serialize_furniture(furniture_obj):
    """Converts a Furniture object to a dictionary for JSON storage."""
    if isinstance(furniture_obj, Furniture):
        furniture_dict = vars(furniture_obj)
        furniture_dict["type"] = type(furniture_obj).__name__  # Store type for deserialization
        return furniture_dict
    return furniture_obj


def deserialize_furniture(furniture_dict):
    """Converts a dictionary back into a Furniture object."""
    if isinstance(furniture_dict, Dict) and "serial_number" in furniture_dict:
        furniture_type = furniture_dict.pop("type", None)
        if furniture_type:
            # Remove any attributes that are not part of the constructor
            allowed_keys = ["name", "description", "price", "dimensions", "serial_number",
                            "quantity", "weight", "manufacturing_country", "has_wheels",
                            "how_many_legs", "can_turn_to_bed", "how_many_seats",
                            "expandable", "can_fold", "has_storage", "has_back",
                            "how_many_doors", "has_mirrors", "number_of_shelves"]

            filtered_dict = {k: v for k, v in furniture_dict.items() if k in allowed_keys}
            return FurnitureFactory.create_furniture({"type": furniture_type, **filtered_dict})
    return furniture_dict


# JSON file as a database
USER_FILE = os.path.join(os.path.join(os.path.dirname(__file__), ".."), "data/users.json")


# -------- USER CLASSES {User,Client,Manager}-------- #
class User(ABC):
    """
    Abstract base class representing a user.

    Attributes:
        user_id (int): Unique identifier for the user.
        username (str): The username of the user.
        email (str): The user's email address.
        password (str): The hashed password.
        address (str): The user's address.
    """

    def __init__(self, user_id, username, email, password, address):
        """
        Initialize a User object.

        param:
            user_id (str): The unique ID of the user.
            username (str): The username of the user.
            email (str): The email address of the user.
            password (str): The user's password (hashed if not already): bytes
            address (str): The user's address.
        """
        self.user_id = str(user_id)
        self.username = username
        self.email = email
        self.password = self.hash_password(password) if not password.startswith("$2b$") else password
        self.address = address

    @staticmethod
    def hash_password(password) -> bytes:
        """
        Hashes the password using bcrypt.

        param:
            password (str): The plain text password.

        return:
            str: The hashed password.
        """
        return bcrypt.hashpw(password, bcrypt.gensalt())

    def verify_password(self, password: str) -> bool | str:
        """
        Verifies if the provided password matches the stored hashed password.

        param:
            password (str): The plain text password.

        return:
            bool: True if password matches.
            str: "Invalid password" if password does not match.
        """
        if bcrypt.checkpw(password.encode(), self.password):
            return True
        return "Invalid password"

    def edit_info(self, username=None, email=None, address=None, password=None):
        """
        Update the user's information.

        param:
            username (str, optional): New username.
            email (str, optional): New email address.
            address (str, optional): New address.
        """
        if username:
            self.username = username
        if email:
            self.email = email
        if address:
            self.address = address
        if password:
            self.password = self.hash_password(password) if not password.startswith("$2b$") else password


class Client(User):
    """
    Represents a client user with a shopping cart.

    Attributes:
        shopping_cart (ShoppingCart): The client's shopping cart.
        type (str): User type identifier ("Client").
    """

    def __init__(self, user_id, username, email, password, address):
        """
        Initialize a Client object.

        param:
            shopping cart [list]: the shopping cart for the client
            type: the type of the user
        """
        super().__init__(user_id, username, email, password, address)
        self.shopping_cart = ShoppingCart(user_id)
        self.type = "Client"

    def user_add_to_cart(self, item, quantity):
        """
        Adds an item_name to the user's shopping cart.

        Args:
            item (Furniture): The item_name to add.
            quantity (int): The number of items to add.
        """
        self.shopping_cart.add_item(item, quantity)

    def user_remove_from_cart(self, item_name: str):
        """
        removes an item to the user's shopping cart.

        Args:
            item_name (Furniture): The item to remove.
            .
        """
        self.shopping_cart.remove_item(item_name)

    def get_cart(self):
        """
        Retrieves the shopping cart.

        Returns:
            ShoppingCart: The client's shopping cart.
        """
        return self.shopping_cart.get_cart()


class Management(User):
    """
    Represents a management-level user.

    Attributes:
        rule (str): The management role.
        type (str): User type identifier ("Management").
    """

    def __init__(self, user_id, username, email, password, address, rule):
        """
        Initialize a Management user.

        param:
            user_id (int): The unique ID of the manager.
            username (str): The username of the manager.
            email (str): The email address of the manager.
            password (str): The password of the manager.
            address (str): The manager's address.
            rule (str): The managerial role.
        """
        super().__init__(user_id, username, email, password, address)
        self.rule = rule
        self.type = "Management"

    def edit_info(self, username=None, email=None, address=None, rule=None):
        """
        Update the management user's information.

        param:
            username (str, optional): New username.
            email (str, optional): New email address.
            address (str, optional): New address.
            rule (str, optional): New managerial role.
        """
        if username:
            self.username = username
        if email:
            self.email = email
        if address:
            self.address = address
        if rule:
            self.rule = rule


# -------- USER DATABASE CLASS -------- #
class UserDB:
    """
    Manages user data storage and retrieval using a JSON file.

    Attributes:
        file_path (str): Path to the user database file.
        user_data (dict): Dictionary containing user objects.
    """

    def __init__(self, file_path=USER_FILE):
        """
        Initialize the UserDB and load users from the JSON file.

        param:
            file_path (str, optional): Path to the JSON file. Default is "users.json".
        """
        self.file_path = file_path
        self.user_data = {}  # Store users in dictionary
        self.load_users()

    def load_users(self):
        """Loads users from the JSON file and converts stored furniture dictionaries back into objects."""

        directory = os.path.dirname(self.file_path)

        if not os.path.exists(directory):  # Ensure the 'data' directory exists
            os.makedirs(directory)  # Create the missing directory

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as file:
                json.dump({}, file, indent=4)
            return

        with open(self.file_path, "r") as file:
            data = json.load(file)

        if not data:
            return

        for user_id, user in data.items():
            type_user = user.pop("type")
            shopping_cart_items = user.pop("shopping_cart", [])

            if type_user == "Client":
                client = Client(**user)
                client.shopping_cart.items = [
                    {"item": deserialize_furniture(i["item"]), "quantity": i["quantity"]}
                    for i in shopping_cart_items
                ]
                self.user_data[int(user_id)] = client
            else:
                self.user_data[int(user_id)] = Management(**user)

    def save_users(self):
        """Saves users to the JSON file, ensuring furniture objects are serializable."""
        with open(self.file_path, "w") as file:
            json.dump(
                {
                    user_id: {
                        **vars(user),
                        "shopping_cart": [
                            {"item_name": serialize_furniture(i["item_name"]), "quantity": i["quantity"]}
                            for i in user.shopping_cart.items
                        ]
                        if hasattr(user, "shopping_cart") else None
                    }
                    for user_id, user in self.user_data.items()
                },
                file, indent=4
            )

    def add_user(self, user) -> str:
        """
        Adds a new user to the database.

        param:
            user (User): The user object to add.

        return:
            str: Success or error message.
        """
        if user.user_id in self.user_data:
            return "User ID already exists in UserDB"
        self.user_data[user.user_id] = user
        self.save_users()
        return "User successfully added!"

    def edit_user(self, user_id, **kwargs):
        """
        Edits an existing user's details.

        param:
            user_id (int): The ID of the user to edit.
            **kwargs: Fields to update (e.g., username, email).

        return:
            str: Success or error message.
        """
        user = self.user_data.get(user_id)
        if not user:
            return "User not found. Please check the ID and try again."
        user.edit_info(**kwargs)
        self.save_users()
        return "User information updated successfully."

    def get_user(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by ID.

        param:
            user_id (int): The ID of the user.

        return:
            User: The user object if found, None otherwise.
        """
        return self.user_data.get(user_id)

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by checking email and password.

        param:
            email (str): The email of the user.
            password (str): The password to verify.

        return:
            User: The authenticated user object if credentials are correct, otherwise None.
        """
        for user in self.user_data.values():
            if user.email == email and user.verify_password(password):
                return user
        return None

    def delete_user(self, user_id: int):
        """
        Deletes a user from the database.

        param:
            user_id (int): The ID of the user to delete.

        return:
            str: Success or error message.
        """
        if user_id not in self.user_data:
            return "User not found. Cannot delete."
        del self.user_data[user_id]
        self.save_users()
        return "User successfully deleted."
