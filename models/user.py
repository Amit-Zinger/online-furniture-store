from abc import ABC, abstractmethod
import bcrypt

class User(ABC):
    users_list = []

    def __init__(self, username, email, password, address):
        self.username = username
        self.email = email
        self.password = self.hash_password(password)
        self.address = address

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    @abstractmethod
    def get_user_type(self):
        pass

    @abstractmethod
    def notify_email(self):
        pass

    @classmethod
    def login(cls, username, password):
        for user in cls.users_list:
            if user.username == username and user.verify_password(password):
                print(f"Login successful for {username}")
                return True
        print("Login failed: Invalid username or password")
        return False

    @classmethod
    def register(cls, username, email, password, address, user_type, **kwargs):
        if any(user.username == username for user in cls.users_list):
            print("Registration failed: Username already exists")
            return None

        if user_type == "Client":
            new_user = Client(username, email, password, address, kwargs.get("client_id"))
        elif user_type == "Management":
            new_user = Management(username, email, password, address, kwargs.get("worker_id"), kwargs.get("role"))
        else:
            print("Invalid user type")
            return None

        cls.users_list.append(new_user)
        print(f"User {username} registered successfully with email {email}")
        return new_user

class Client(User):
    def __init__(self, username, email, password, address, client_id):
        super().__init__(username, email, password, address)
        self.client_id = client_id
        self.shop_cart = []
        self.liked_list = []

    def get_user_type(self):
        return "Client"

    def notify_email(self):
        print(f"Notification sent to {self.email}")

    def get_order_history(self):
        print("Order history retrieved.")

    def get_client_info(self):
        return {
            "username": self.username,
            "email": self.email,
            "address": self.address,
            "client_id": self.client_id
        }

    def edit_client_info(self, new_username=None, new_email=None, new_address=None):
        if new_username:
            self.username = new_username
        if new_email:
            self.email = new_email
        if new_address:
            self.address = new_address
        print("Client info updated successfully.")

    def add_cart(self, item):
        self.shop_cart.append(item)
        print(f"{item} added to cart.")

    def like_product(self, product):
        self.liked_list.append(product)
        print(f"{product} liked.")

    def dislike_product(self, product):
        if product in self.liked_list:
            self.liked_list.remove(product)
            print(f"{product} removed from liked list.")

class Management(User):
    def __init__(self, username, email, password, address, worker_id, role):
        super().__init__(username, email, password, address)
        self.worker_id = worker_id
        self.role = role

    def get_user_type(self):
        return "Management"

    def notify_email(self):
        print(f"Notification sent to management email {self.email}")

    def check_inventory(self):
        print("Inventory checked.")

    def check_low_inventory(self):
        print("Low inventory items retrieved.")
