import json
import os
import sys
import bcrypt
from abc import ABC
from typing import Dict, Optional
from models.cart import ShoppingCart
from models.furniture import Furniture
from models.factory import FurnitureFactory

# Ensure the parent directory is in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# -------- Helper Func -------- #
def serialize_furniture(furniture_obj):
    """
    Converts a Furniture object to a dictionary for JSON storage.

    param:
        furniture_obj (Furniture): The furniture object to serialize.

    return:
        dict: Dictionary representation of the furniture object.
    """
    if isinstance(furniture_obj, Furniture):
        furniture_dict = vars(furniture_obj)
        furniture_dict["type"] = type(
            furniture_obj
        ).__name__  # Store type for deserialization
        return furniture_dict
    return furniture_obj


def deserialize_furniture(furniture_dict):
    """
    Converts a dictionary back into a Furniture object.

    param:
        furniture_dict (dict): Dictionary representation of a furniture object.

    return:
        Furniture: Deserialized Furniture object.
    """
    if isinstance(furniture_dict, Dict) and "serial_number" in furniture_dict:
        furniture_type = furniture_dict.pop("type", None)
        if furniture_type:
            # Remove any attributes that are not part of the constructor
            allowed_keys = [
                "name",
                "description",
                "price",
                "dimensions",
                "serial_number",
                "quantity",
                "weight",
                "manufacturing_country",
                "has_wheels",
                "how_many_legs",
                "can_turn_to_bed",
                "how_many_seats",
                "expandable",
                "can_fold",
                "has_storage",
                "has_back",
                "how_many_doors",
                "has_mirrors",
                "number_of_shelves",
            ]

            filtered_dict = {
                k: v for k, v in furniture_dict.items() if k in allowed_keys
            }
            return FurnitureFactory.create_furniture(
                {"type": furniture_type, **filtered_dict}
            )
    return furniture_dict


# Define the default users DB path
USER_FILE = os.path.join(
    os.path.join(os.path.dirname(__file__), ".."), "data/users.json"
)


# -------- USER CLASSES {User,Client,Manager}-------- #
class User(ABC):
    """
    Abstract base class representing a user.

    Attributes:
        user_id (str): The ID for the user.
        username (str): The username of the user - Unique identifier.
        email (str): The user's email address.
        password (str): The hashed password.
        address (str): The user's address.
    """

    def __init__(
        self, user_id: int, username: str, email: str, password: str, address: str
    ) -> None:
        """
        Initialize a User object.

        param:
            user_id (int): The ID of the user.
            username (str): The unique username of the user.
            email (str): The email address of the user.
            password (str): The user's password (hashed if not already): bytes
            address (str): The user's address.
        """
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = (
            self.hash_password(password)
            if not password.startswith("$2b$")
            else password
        )
        self.address = address

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes the password using bcrypt.

        param:
            password (str): The plain text password.

        return:
            str: The hashed password.
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def verify_password(self, password: str) -> bool:
        """
        Verifies if the provided password matches the stored hashed password.

        param:
            password (str): The plain text password.

        return:
            bool: True if password matches.

        """
        return bcrypt.checkpw(password.encode(), self.password.encode())

    def change_password(self, new_password: str) -> None:
        """
        Changes the user's password, encrypts it, and updates the database.

        param:
            new_password (str): The new password to be set.
        """
        self.password = User.hash_password(new_password)

        user_db = UserDB.get_instance()
        if self.user_id in user_db.user_data:
            user_db.user_data[self.user_id] = self
            user_db.save_users()

    def edit_info(
        self,
        username: Optional[str] = None,
        email: Optional[str] = None,
        address: Optional[str] = None,
    ) -> None:
        """
        Edits the user's information.

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
        user_db = UserDB.get_instance()
        if self.user_id in user_db.user_data:
            user_db.user_data[self.user_id] = self
            user_db.save_users()


class Client(User):
    """
    Represents a client user with a shopping cart
    Attributes:
        shopping_cart (ShoppingCart): The client's shopping cart.
        type (str): User type identifier ("Client").
    """

    def __init__(
        self, user_id: int, username: str, email: str, password: str, address: str
    ) -> None:
        """
        Initialize a Client object.

        param:
            shopping cart [list]: the shopping cart for the client
            type: the type of the user
        """
        super().__init__(user_id, username, email, password, address)
        self.shopping_cart = ShoppingCart(str(user_id))
        self.type = "Client"


class Management(User):
    """
    Represents a management-level user.

    Attributes:
        role (str): The management role.
        type (str): User type identifier ("Management").
    """

    def __init__(
        self,
        user_id: int,
        username: str,
        email: str,
        password: str,
        address: str,
        role: str,
    ) -> None:
        """
        Initialize a Management user.

        param:
            user_id (int): The ID of the manager.
            username (str): The unique username of the manager.
            email (str): The email address of the manager.
            password (str): The password of the manager.
            address (str): The manager's address.
            role (str): The managerial role.
        """
        super().__init__(user_id, username, email, password, address)
        self.role = role
        self.type = "Management"

    def edit_role(self, role: Optional[str] = None) -> None:
        """
        Update the management user's role.
        param:
            role (str, optional): New managerial role.
        """
        if role:
            self.role = role
        user_db = UserDB.get_instance()
        if self.user_id in user_db.user_data:
            user_db.user_data[self.user_id] = self
            user_db.save_users()


# -------- USER DATABASE CLASS -------- #
class UserDB:
    """
    Singleton class to manage user data storage and retrieval.
    """

    _instance = None  # Singleton

    @staticmethod
    def get_instance():
        """
        Returns the single instance of UserDB.

        return:
            UserDB: The singleton instance of UserDB.
        """

        if UserDB._instance is None:
            UserDB._instance = UserDB()
        return UserDB._instance

    def __init__(self, file_path: str = USER_FILE) -> None:
        """
        Initialize the UserDB and ensure only one instance exists.

        param:
              file_path (str): Path to the user database file.
        """

        if UserDB._instance is not None:
            raise Exception(
                "Use UserDB.get_instance() instead of creating a new instance."
            )
        self.file_path = file_path
        self.user_data: dict[int, User] = {}
        self.load_users()

    def load_users(self) -> None:
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
                    {
                        "item": deserialize_furniture(i["item"]),
                        "quantity": i["quantity"],
                    }
                    for i in shopping_cart_items
                ]
                self.user_data[user_id] = client
            else:
                self.user_data[user_id] = Management(**user)

    def save_users(self) -> None:
        """Saves users to the JSON file, ensuring furniture objects are serializable."""
        with open(self.file_path, "w") as file:
            json.dump(
                {
                    user_id: {
                        **vars(user),
                        "shopping_cart": (
                            [
                                {
                                    "item": serialize_furniture(i["item"]),
                                    "quantity": i["quantity"],
                                }
                                for i in user.shopping_cart.items
                            ]
                            if hasattr(user, "shopping_cart")
                            else None
                        ),
                    }
                    for user_id, user in self.user_data.items()
                },
                file,
                indent=4,
            )

    def get_user(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by ID.

        param:
            user_id (int): The ID of the user.

        return:
            User: The user object if found, None otherwise.
        """
        return self.user_data.get(user_id)

    def add_user(self, user: User) -> bool:
        """
        Adds a new user to the database.

        param:
            user (User): The user object to add.

        return:
            True if user added and False if not.
        """
        for temp_user in self.user_data.values():
            if user.username == temp_user.username:
                print("User name already exists in UserDB")
                return False

        self.user_data[user.user_id] = user  # Store as string key
        self.save_users()
        print("User successfully added!")
        return True

    def delete_user(self, user_id: int) -> bool:
        """
        Deletes a user from the database.

        param:
            user_id (int): The ID of the user to delete.

        return:
            True if user deleted and False if not.
        """
        if user_id not in self.user_data:
            print("User not found. Cannot delete.")
            return False
        del self.user_data[user_id]
        self.save_users()
        print("User successfully deleted.")
        return True

    def edit_user(self, user_id: int, **kwargs) -> bool:
        """
        Edits an existing user's details.

        param:
            user_id (int): The ID of the user to edit.
            **kwargs: Fields to update (e.g., username, email).

        return:
            True if edit user successfully and False if not.
        """
        user = self.user_data.get(user_id)
        if not user:
            print("User not found. Please check the ID and try again.")
            return False

        if "username" in kwargs:
            for temp_user in self.user_data.values():
                if kwargs["username"] == temp_user.username:
                    print("User name already exists in UserDB")
                    return False

        user.edit_info(**kwargs)
        self.save_users()
        print("User information updated successfully.")
        return True
