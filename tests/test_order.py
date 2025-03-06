import unittest
from unittest.mock import MagicMock
import pandas as pd
import json
import os
import sys
from io import StringIO
from models.order import OrderManager
from models.cart import ShoppingCart
from models.furniture import Furniture


class TestOrderManager(unittest.TestCase):
    """
    Unit tests for the OrderManager class.
    """

    def setUp(self):
        """
        Ensures each test starts with a fresh order list by deleting the saved pickle file.
        """
        # Correct the typo in the test file path
        self.test_orders_file = os.path.join(
            os.path.dirname(__file__), "..", "tests/test_orders.pkl"
        )

        # Initialize OrderManager with the test file path
        self.order_manager = OrderManager(file_path=self.test_orders_file)

        # Ensure the test directory exists
        os.makedirs(os.path.dirname(self.test_orders_file), exist_ok=True)

        # Remove any existing test orders file to prevent test data accumulation
        if os.path.exists(self.test_orders_file):
            os.remove(self.test_orders_file)

        # Force a clean DataFrame to reset test state
        self.order_manager.orders = pd.DataFrame(
            columns=[
                "order_id",
                "client_id",
                "items",
                "total_price",
                "payment_info",
                "status",
                "order_date",
            ]
        )

        self.mock_cart = MagicMock(spec=ShoppingCart)
        self.mock_cart.user_id = 1
        self.mock_cart.items = [
            Furniture(
                name="Table",
                description="Wooden table",
                price=100.0,
                dimensions="120x60 cm",
                serial_number="F123",
                quantity=2,
                weight=15.0,
                manufacturing_country="USA",
            ),
            Furniture(
                name="Chair",
                description="Office chair",
                price=50.0,
                dimensions="50x50 cm",
                serial_number="C456",
                quantity=4,
                weight=7.0,
                manufacturing_country="Germany",
            ),
        ]

    def test_create_order(self):
        """
        Tests order creation and validation of stored data.
        """
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
        """
        Tests retrieving an order by ID and client ID.
        """
        self.order_manager.create_order(self.mock_cart, "Credit Card", 300.0)
        order_id = self.order_manager.orders.iloc[0]["order_id"]
        retrieved_order = self.order_manager.get_order(order_id, 1)
        self.assertIsNotNone(retrieved_order)
        self.assertEqual(retrieved_order["client_id"], 1)

    def test_get_order_not_found(self):
        """
        Tests retrieving a non-existing order.
        """
        order = self.order_manager.get_order("non_existing_id", 1)
        self.assertIsNone(order)

    def test_update_order_status(self):
        """
        Tests updating an order status.
        """
        self.order_manager.create_order(self.mock_cart, "Credit Card", 300.0)
        order_id = self.order_manager.orders.iloc[0]["order_id"]
        self.order_manager.update_order_status(order_id, "Shipped")
        self.assertEqual(
            self.order_manager.orders.loc[
                self.order_manager.orders["order_id"] == order_id, "status"
            ].values[0],
            "Shipped",
        )

    def test_cancel_order(self):
        """
        Tests canceling an order.
        """
        self.order_manager.create_order(self.mock_cart, "Credit Card", 300.0)
        order_id = self.order_manager.orders.iloc[0]["order_id"]
        self.order_manager.cancel_order(order_id)
        self.assertEqual(
            self.order_manager.orders.loc[
                self.order_manager.orders["order_id"] == order_id, "status"
            ].values[0],
            "Cancelled",
        )

    def test_get_order_history(self):
        """
        Tests retrieving order history for a client.
        """
        self.order_manager.create_order(self.mock_cart, "Credit Card", 300.0)
        history = self.order_manager.get_order_history(1)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["client_id"], 1)

    def test_get_order_history_empty(self):
        """
        Tests retrieving order history for a client with no orders.
        """
        history = self.order_manager.get_order_history(2)
        self.assertEqual(len(history), 0)

    def test_order_persistence(self):
        """
        Tests that orders persist after being saved and reloaded.
        """
        self.order_manager.create_order(self.mock_cart, "Credit Card", 300.0)
        order_id = self.order_manager.orders.iloc[0]["order_id"]

        # Ensure the new instance loads from the same test file
        new_order_manager = OrderManager(file_path=self.test_orders_file)

        self.assertIn(order_id, new_order_manager.orders["order_id"].values)

    @classmethod
    def tearDownClass(cls):
        """
        Ensures that the test order pickle file is deleted after all tests have run.
        """
        test_orders_file = os.path.join(
            os.path.dirname(__file__), "..", "tests/test_orders.pkl"
        )

        if os.path.exists(test_orders_file):
            os.remove(test_orders_file)


if __name__ == "__main__":
    unittest.main()
