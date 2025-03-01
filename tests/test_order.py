import unittest
import io
import sys
from models.order import OrderManager
from models.cart import ShoppingCart
from models.furniture import Chair

class TestOrderManager(unittest.TestCase):
    def setUp(self):
        """Set up OrderManager and a sample ShoppingCart with items."""
        self.order_manager = OrderManager()
        self.client_id = "user123"
        # Create sample furniture items.
        self.item1 = Chair(
            name="Office Chair",
            description="Ergonomic chair",
            price=150.0,
            dimensions="50x50x100cm",
            serial_number="CH001",
            quantity=10,
            weight=10,
            manufacturing_country="Germany",
            has_wheels=True,
            how_many_legs=5,
        )
        self.item2 = Chair(
            name="Gaming Chair",
            description="Comfortable gaming chair",
            price=200.0,
            dimensions="55x55x110cm",
            serial_number="CH002",
            quantity=5,
            weight=12,
            manufacturing_country="USA",
            has_wheels=True,
            how_many_legs=5,
        )
        # Create a shopping cart for our client.
        self.cart = ShoppingCart(self.client_id)
        self.cart.add_item(self.item1, 2)
        self.cart.add_item(self.item2, 1)
        self.total_price = self.cart.calculate_total()  # (150*2)+(200*1) = 500

    def test_create_order(self):
        """Test that an order is correctly created and added."""
        self.order_manager.create_order(self.cart, "dummy_payment", self.total_price)
        self.assertEqual(len(self.order_manager.orders), 1)
        order_data = self.order_manager.orders.iloc[0]
        self.assertEqual(order_data["client_id"], self.client_id)
        self.assertEqual(order_data["payment_info"], "dummy_payment")
        self.assertEqual(order_data["total_price"], self.total_price)
        self.assertEqual(order_data["status"], "Processing")
        # Check that the items recorded match the cart's items.
        self.assertEqual(order_data["items"], self.cart.items)

    def test_get_order(self):
        """Test retrieving an order by order_id and client_id."""
        self.order_manager.create_order(self.cart, "dummy_payment", self.total_price)
        order_id = self.order_manager.orders.iloc[0]["order_id"]
        order = self.order_manager.get_order(order_id, self.client_id)
        self.assertIsNotNone(order)
        self.assertEqual(order["order_id"], order_id)
        # Test with wrong client_id returns None.
        order_wrong = self.order_manager.get_order(order_id, "wrong_client")
        self.assertIsNone(order_wrong)

    def test_update_order_status(self):
        """Test updating the status of an order."""
        self.order_manager.create_order(self.cart, "dummy_payment", self.total_price)
        order_id = self.order_manager.orders.iloc[0]["order_id"]
        self.order_manager.update_order_status(order_id, "Shipped")
        updated_order = self.order_manager.get_order(order_id, self.client_id)
        self.assertEqual(updated_order["status"], "Shipped")

    def test_cancel_order(self):
        """Test cancelling an order."""
        self.order_manager.create_order(self.cart, "dummy_payment", self.total_price)
        order_id = self.order_manager.orders.iloc[0]["order_id"]
        self.order_manager.cancel_order(order_id)
        cancelled_order = self.order_manager.get_order(order_id, self.client_id)
        self.assertEqual(cancelled_order["status"], "Cancelled")

    def test_get_order_history(self):
        """Test retrieval of order history for a client."""
        # Create two orders for the same client.
        self.order_manager.create_order(self.cart, "payment1", self.total_price)
        self.order_manager.create_order(self.cart, "payment2", self.total_price)
        # Create another order for a different client.
        other_cart = ShoppingCart("other_user")
        other_cart.add_item(self.item1, 1)
        self.order_manager.create_order(other_cart, "payment3", other_cart.calculate_total())
        history = self.order_manager.get_order_history(self.client_id)
        self.assertEqual(len(history), 2)
        other_history = self.order_manager.get_order_history("other_user")
        self.assertEqual(len(other_history), 1)

    def test_update_observer(self):
        """Test that update_observer produces the expected output."""
        self.order_manager.create_order(self.cart, "dummy_payment", self.total_price)
        order_id = self.order_manager.orders.iloc[0]["order_id"]
        # Capture printed output.
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.order_manager.update_observer(order_id)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Notifying observers", output)

if __name__ == "__main__":
    unittest.main()
