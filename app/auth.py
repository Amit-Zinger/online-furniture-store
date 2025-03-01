from flask import Flask
from flask_login import LoginManager, UserMixin, login_user, logout_user
from models.cart import ShoppingCart
from models.user import UserDB, Client, Management

app = Flask(__name__)
app.secret_key = "your_secret_key"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, user_id):
        user_db = UserDB()
        user_data = user_db.get_user(user_id)
        if not user_data:
            raise ValueError("User not found")

        self.id = user_data.id
        self.username = user_data.username
        self.email = user_data.email
        self.address = user_data.address
        self.role = user_data.get("role", "client")
        self.cart = ShoppingCart(user_id)

    def is_manager(self):
        """Check if the user is a manager."""
        return self.role == "Management"

@login_manager.user_loader
def load_user(user_id):
    """Flask-Login function to load a user by ID."""
    user_db = UserDB()
    user = user_db.get_user(int(user_id))
    if user:
        if user.type == "Client":
            return Client(user.id, user.username, user.email, user.password, user.address)
        elif user.type == "Management":
            return Management(user.id, user.username, user.email, user.password, user.address, user.rule)
    return None

def login(username, password):
    """Authenticate and login a user."""
    user_db = UserDB()
    user = user_db.authenticate_user(username, password)
    if user:
        if user.type == "Client":
            login_user(Client(user.id, user.username, user.email, user.password, user.address))
        elif user.type == "Management":
            login_user(Management(user.id, user.username, user.email, user.password, user.address, user.rule))
        return True
    return False

def logout():
    """Logout the current user."""
    logout_user()

# Load and save user data functions
def load_user_data():
    """Load user data from a JSON file."""
    return UserDB().get_all_users()

def save_user_data(data):
    """Save user data to a JSON file."""
    user_db = UserDB()
    user_db.user_data = data
    user_db.save_users()
