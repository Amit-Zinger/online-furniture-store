from flask_login import UserMixin
from models.cart import ShoppingCart


class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.cart = ShoppingCart(username)


# Load and save user data functions
def load_user_data():
    """Load user data from a JSON file."""
    data = load_data()
    return data["users"]


def save_user_data(data):
    """Save user data to a JSON file."""
    save_data(data)

