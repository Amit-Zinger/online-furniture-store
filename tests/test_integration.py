import pytest
from models.user import Client, UserDB, USER_FILE
from models.cart import ShoppingCart, PaymentGateway
from models.inventory import Inventory
from models.order import OrderManager
from models.factory import FurnitureFactory
import os
import tempfile
from app.utils import serialize_furniture, deserialize_furniture  # ✅ Ensure correct import


@pytest.fixture(scope="function")
def setup_system():
    """Sets up a full system with users, cart, inventory, and order management."""
    # Ensure a fresh start by deleting users.json
    if os.path.exists(USER_FILE):
        os.remove(USER_FILE)

    # Temporary inventory file
    inventory_file = tempfile.mktemp(suffix=".pkl")
    inventory = Inventory(inventory_file)

    # Create user database
    user_db = UserDB()
    client = Client(id=1, username="test_client", email="client@test.com", password="password123", address="123 Street")
    user_db.add_user(client)

    # Create order manager
    order_manager = OrderManager()

    return user_db, inventory, order_manager, inventory_file


def test_client_shopping_cart_persistence(setup_system):
    """Test that a client's cart persists after being saved and loaded."""
    user_db, _, _, _ = setup_system
    client = user_db.get_user(1)

    # Add item to cart
    item_desc = {
        "type": "Chair",
        "name": "Test Chair",
        "description": "Comfortable chair",
        "price": 100.0,
        "dimensions": "50x50x100 cm",
        "serial_number": "CH999",
        "quantity": 10,
        "weight": 15.0,
        "manufacturing_country": "Germany",
        "has_wheels": True,
        "how_many_legs": 4,
    }
    item = FurnitureFactory.create_furniture(item_desc)
    client.shopping_cart.add_item(item, 1)

    # ✅ Save users (handles serialization properly)
    user_db.save_users()

    # ✅ Reload users (handles deserialization properly)
    new_user_db = UserDB()
    new_client = new_user_db.get_user(1)

    assert len(new_client.shopping_cart.get_cart()) == 1  # Ensure persistence


def test_purchase_reduces_inventory(setup_system):
    """Test that purchasing an item correctly reduces inventory stock."""
    user_db, inventory, order_manager, _ = setup_system
    client = user_db.get_user(1)

    # ✅ Add item to inventory
    item_desc = {
        "type": "Chair",
        "name": "Office Chair",
        "description": "Comfortable chair",
        "price": 150.0,
        "quantity": 5,
        "serial_number": "CH001",
        "dimensions": "50x50x100 cm",
        "weight": 15.0,
        "manufacturing_country": "Germany",
        "has_wheels": True,
        "how_many_legs": 5,
    }
    inventory.add_item(item_desc.copy())

    # ✅ Add item to cart
    item = FurnitureFactory.create_furniture(item_desc.copy())
    client.shopping_cart.add_item(item, 2)

    # ✅ Fix: Pass `payment_gateway` along with `inventory` and `order_manager`
    payment_gateway = PaymentGateway()
    client.shopping_cart.purchase(payment_gateway, "dummy_payment_info", inventory, order_manager)

    # ✅ Ensure inventory update after purchase
    updated_items = inventory.search_by(name="Office Chair")
    assert updated_items[0].quantity == 3  # Original 5 - Purchased 2


def test_order_created_after_successful_purchase(setup_system):
    """Test that a successful purchase creates an order entry."""
    user_db, inventory, order_manager, _ = setup_system
    client = user_db.get_user(1)

    # ✅ Add item to inventory
    item_desc = {
        "type": "Chair",
        "name": "Office Chair",
        "description": "Comfortable chair",
        "price": 150.0,
        "quantity": 5,
        "serial_number": "CH001",
        "dimensions": "50x50x100 cm",
        "weight": 15.0,
        "manufacturing_country": "Germany",
        "has_wheels": True,
        "how_many_legs": 5,
    }
    inventory.add_item(item_desc.copy())

    # ✅ Add item to cart
    item = FurnitureFactory.create_furniture(item_desc.copy())
    client.shopping_cart.add_item(item, 2)

    # ✅ Fix: Pass `payment_gateway`, `inventory`, and `order_manager`
    payment_gateway = PaymentGateway()
    client.shopping_cart.purchase(payment_gateway, "dummy_payment_info", inventory, order_manager)

    # ✅ Ensure order is created in OrderManager
    assert len(order_manager.orders) == 1




