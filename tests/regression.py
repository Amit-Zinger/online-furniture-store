import os
import sys
from typing import Dict, Optional, List, Tuple
from models.user import Client, UserDB
from models.cart import PaymentGateway
from models.inventory import Inventory
from models.order import OrderManager

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..")))

# Define test database file paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
USER_FILE = os.path.join(DATA_DIR, "test_users.json")
INVEN_FILE = os.path.join(DATA_DIR, "test_inventory.pkl")
ORDER_FILE = os.path.join(DATA_DIR, "test_orders.pkl")


def setup_system() -> Tuple[UserDB, Inventory, OrderManager]:
    """
    Sets up a full system with users, inventory, and order management.

    return:
        Tuple[UserDB, Inventory, OrderManager]: Initialized user database, inventory, and order manager.
    """
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Remove old test files
    for file_path in [USER_FILE, INVEN_FILE, ORDER_FILE]:
        if os.path.exists(file_path):
            os.remove(file_path)

    # Create Inventory object
    inventory = Inventory(INVEN_FILE)

    # Create multiple furniture items
    furniture_items = [
        {
            "type": "Chair",
            "name": "Office Chair",
            "description": "Ergonomic chair",
            "price": 120.0,
            "quantity": 10,
            "serial_number": "CH001",
            "has_wheels": False,
            "how_many_legs": 4,
            "weight": 25,
            "manufacturing_country": "USA",
            "dimensions": "100x50x75 cm",
        },
        {
            "type": "Table",
            "name": "Dining Table",
            "description": "Wooden dining table",
            "price": 300.0,
            "quantity": 5,
            "serial_number": "TB001",
            "expandable": False,
            "how_many_seats": 4,
            "can_fold": False,
            "weight": 25,
            "manufacturing_country": "USA",
            "dimensions": "100x50x75 cm",
        },
        {
            "type": "Sofa",
            "name": "Leather Sofa",
            "description": "Comfortable leather sofa",
            "price": 700.0,
            "quantity": 3,
            "serial_number": "SF001",
            "can_turn_to_bed": True,
            "how_many_seats": 3,
            "weight": 25,
            "manufacturing_country": "USA",
            "dimensions": "100x50x75 cm",
        },
    ]

    for item in furniture_items:
        inventory.add_item(item)
    inventory.update_data()

    # Create multiple users
    user_db = UserDB(USER_FILE)
    users = [
        Client(
            user_id=1,
            username="test_client",
            email="client1@test.com",
            password="password123",
            address="123 Street",
        ),
        Client(
            user_id=2,
            username="client2",
            email="client2@test.com",
            password="password456",
            address="456 Avenue",
        ),
    ]
    for user in users:
        user_db.add_user(user)

    # Create OrderManger object
    order_manager = OrderManager(ORDER_FILE)

    print("System setup completed.")
    return user_db, inventory, order_manager


def search_product_in_inventory(
    inventory: Inventory, product_name: str
) -> Optional[object]:
    """
    Search for a product in inventory and return it.

    param:
        inventory (Inventory): The inventory instance to search.
        product_name (str): The name of the product to search for.

    return:
        Optional[object]: The found product or None if not found.
    """
    results = inventory.search_by(name=product_name)
    return results[0] if results else None


def add_to_cart(client: Client, product: object, quantity: int) -> bool:
    """
    Add a product to the user's cart.

    param:
        client (Client): The client adding the item to their cart.
        product (object): The furniture product to add.
        quantity (int): The quantity to add.

    return:
        bool: True if add was successful, False otherwise.
    """
    # Add the bool option to add_item
    if not (client.shopping_cart.add_item(product, quantity)):
        return False
    return True


def checkout(client: Client, inventory: Inventory,
             order_manager: OrderManager) -> bool:
    """
    Process checkout and update inventory and orders.

    param:
        client (Client): The client making the purchase.
        inventory (Inventory): The inventory instance to update.
        order_manager (OrderManager): The order manager handling the purchase.

    return:
        bool: True if checkout was successful, False otherwise.
    """
    payment_gateway = PaymentGateway()
    if client.shopping_cart.get_cart():
        client.shopping_cart.purchase(
            payment_gateway, "dummy_payment_info", inventory, order_manager
        )
        print("Checkout successful. Order created and inventory updated.")
        return True
    print("Cart is empty. Checkout failed.")
    return False


def verify_updates(inventory: Inventory,
                   order_manager: OrderManager,
                   purchased_items: Dict[str,
                                         int]) -> None:
    """
    Verify if inventory and order database are updated correctly.

    param:
        inventory (Inventory): The inventory instance.
        order_manager (OrderManager): The order manager instance.
        purchased_items (Dict[str, int]): Dictionary of purchased items with expected quantities.

    """
    for item_name, expected_quantity in purchased_items.items():
        updated_item = inventory.search_by(name=item_name)[0]
        if updated_item.quantity != expected_quantity:
            print(f"Inventory update failed for {item_name}.")
            return
    print("Inventory updated correctly.")

    if len(order_manager.orders.index) > 0:
        print("OrderManger updated correctly.")
    else:
        print("OrderManger update failed.")


def check_other_inventory_unchanged(
    original_inventory: List[object],
    updated_inventory: Inventory,
    modified_items: List[str],
) -> None:
    """
    Ensure that only the purchased items were changed and others remained the same.

    param:
        original_inventory (List[object]): List of original inventory items before the purchase.
        updated_inventory (Inventory): The updated inventory instance after the purchase.
        modified_items (List[str]): List of item names that were modified.

    """
    for furniture_item in original_inventory:
        if furniture_item.name not in modified_items:
            updated_item = updated_inventory.search_by(
                name=furniture_item.name)[0]
            if updated_item != furniture_item:
                print(
                    f"Unexpected change detected for {
                        furniture_item.name} in inventory.")
                return
    print(f"Inventory DB for other objects remained unchanged for .")


def cleanup_system() -> None:
    """
    Removes test data files after execution.
    """
    for file_path in [USER_FILE, INVEN_FILE, ORDER_FILE]:
        if os.path.exists(file_path):
            os.remove(file_path)
    print("Test files cleaned up.")


def run_tests() -> None:
    """
    Runs all system integration tests.
    """
    user_db, inventory, order_manager = setup_system()
    client = user_db.get_user(1)
    original_inventory = inventory.search_by()

    print("-------Starting Test----------")

    purchases = {"Office Chair": 2, "Dining Table": 1}

    for item_name, qty in purchases.items():
        product = search_product_in_inventory(inventory, item_name)
        if not product:
            print("Search in Inventory failed in test.")
            return
        if not add_to_cart(client, product, qty):
            print("Failed to add item to user ShoppingCart.")
            return
    print(
        "Search in Inventory furniture objects ended successfully.\nAdding furniture objects "
        "to ShoppingCart ended successfully")

    if checkout(client, inventory, order_manager):
        verify_updates(
            inventory, order_manager, {
                "Office Chair": 8, "Dining Table": 4})
        check_other_inventory_unchanged(
            original_inventory, inventory, purchases.keys())

    # Once a day the system should update the databsaes file - demonstartion
    # of it
    inventory.update_data()
    user_db.save_users()
    order_manager.save_orders()
    print("Updated database files succfully.")

    cleanup_system()


if __name__ == "__main__":
    run_tests()
