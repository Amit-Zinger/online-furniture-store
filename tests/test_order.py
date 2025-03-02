import unittest
from unittest.mock import MagicMock
import pandas as pd
import json
from models.order import OrderManager
from models.cart import ShoppingCart
from io import StringIO
import sys

class TestOrderManager(unittest.TestCase):
    def setUp(self):
        self.order_manager = OrderManager()
        self.mock_cart = MagicMock(spec=ShoppingCart)
        self.mock_cart.user_id = 1
        self.mock_cart.items = [
            {"item": MagicMock(id=101, name="Table", price=100.0), "quantity": 2},
            {"item": MagicMock(id=102, name="Chair", price=50.0), "quantity": 4}
        ]

    def test_create_order(self):
        self.order_manager.create_order(self.mock_cart, "Credit Card", 300.0)
        self.assertEqual(len(self.order_manager.orders), 1)
        order = self.order_manager.orders.iloc[0]
        self.assertEqual(order["client_id"], 1)
        self.assertEqual(order["total_price"], 300.0)
        self.assertEqual(order["status"], "Processing")
        self.assertIsInstance(order["order_date"], str)
        items = json.loads(order["items"])
        self.assertEqual(len(items), 2)

    def test_get_order(self):
        self.order_manager.create_order(self.mock_cart, "Credit Card", 300.0)
        order_id = self.order_manager.orders.iloc[0]["order_id"]
        retrieved_order = self.order_manager.get_order(order_id, 1)
        self.assertIsNotNone(retrieved_order)
        self.assertEqual(retrieved_order["client_id"], 1)

    def test_get_order_not_found(self):
        order = self.order_manager.get_order("non_existing_id", 1)
        self.assertIsNone(order)

    def test_update_order_status(self):
        self.order_manager.create_order(self.mock_cart, "Credit Card", 300.0)
        order_id = self.order_manager.orders.iloc[0]["order_id"]
        self.order_manager.update_order_status(order_id, "Shipped")
        self.assertEqual(self.order_manager.orders.loc[self.order_manager.orders["order_id"] == order_id, "status"].values[0], "Shipped")

    def test_cancel_order(self):
        self.order_manager.create_order(self.mock_cart, "Credit Card", 300.0)
        order_id = self.order_manager.orders.iloc[0]["order_id"]
        self.order_manager.cancel_order(order_id)
        self.assertEqual(self.order_manager.orders.loc[self.order_manager.orders["order_id"] == order_id, "status"].values[0], "Cancelled")

    def test_get_order_history(self):
        self.order_manager.create_order(self.mock_cart, "Credit Card", 300.0)
        history = self.order_manager.get_order_history(1)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["client_id"], 1)

    def test_get_order_history_empty(self):
        history = self.order_manager.get_order_history(2)
        self.assertEqual(len(history), 0)

    def test_update_observer(self):
        self.order_manager.create_order(self.mock_cart, "Credit Card", 300.0)
        order_id = self.order_manager.orders.iloc[0]["order_id"]
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        self.order_manager.update_observer(order_id)
        sys.stdout = sys.__stdout__  # Reset stdout
        output = captured_output.getvalue()
        self.assertIn(f"Order {order_id} status is now Processing. Notifying observers...", output)

if __name__ == "__main__":
    unittest.main()
