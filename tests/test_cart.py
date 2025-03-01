import unittest
import tempfile
import os
from models.cart import ShoppingCart, PaymentGateway
from models.furniture import Chair
from models.inventory import Inventory

class TestShoppingCart(unittest.TestCase):

    def setUp(self):
        """Set up a shopping cart and a real inventory before each test."""
        self.cart = ShoppingCart("user123")
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
        # Create a temporary file path for the inventory pickle file.
        self.inventory_file = tempfile.mktemp(suffix=".pkl")
        self.inventory = Inventory(self.inventory_file)
        # Reset the inventory for Chairs and add our test items.
        self.inventory.data.at[0, "Chair"] = []  # Clear existing list.
        self.inventory.data.at[0, "Chair"].append(self.item1)
        self.inventory.data.at[0, "Chair"].append(self.item2)
        self.inventory.update_data()

    def tearDown(self):
        """Clean up the temporary inventory file."""
        if os.path.exists(self.inventory_file):
            os.remove(self.inventory_file)

    def test_add_item(self):
        """Test adding items to the cart."""
        self.cart.add_item(self.item1, 2)
        cart_contents = self.cart.get_cart()
        self.assertEqual(len(cart_contents), 1)
        self.assertEqual(cart_contents[0]["quantity"], 2)

    def test_remove_item(self):
        """Test removing an item from the cart."""
        self.cart.add_item(self.item1, 1)
        self.cart.remove_item(self.item1.name)
        self.assertEqual(len(self.cart.get_cart()), 0)

    def test_calculate_total(self):
        """Test total price calculation of the cart."""
        self.cart.add_item(self.item1, 2)
        self.cart.add_item(self.item2, 1)
        # (150*2) + (200*1) = 300 + 200 = 500
        self.assertEqual(self.cart.calculate_total(), 500.0)

    def test_apply_discount(self):
        """Test applying a discount to the cart."""
        self.cart.add_item(self.item1, 2)
        # Total is 300; a 10% discount should yield 270.
        discounted_total = self.cart.apply_discount(10)
        self.assertEqual(discounted_total, 270.0)

    def test_clear_cart(self):
        """Test clearing the cart."""
        self.cart.add_item(self.item1, 2)
        self.cart.clear_cart()
        self.assertEqual(len(self.cart.get_cart()), 0)

    def test_validate_cart_with_inventory_success(self):
        """Test that cart validation passes when inventory is sufficient."""
        self.cart.add_item(self.item1, 2)
        valid = self.cart.validate_cart(self.inventory)
        self.assertTrue(valid)

    def test_validate_cart_with_inventory_failure(self):
        """Test that cart validation fails when inventory is insufficient."""
        self.cart.add_item(self.item1, 11)  # item1 has only 10 available.
        valid = self.cart.validate_cart(self.inventory)
        self.assertFalse(valid)

    def test_update_inventory(self):
        """Test that update_inventory correctly adjusts the inventory quantity."""
        self.cart.add_item(self.item1, 2)
        self.cart.update_inventory(self.inventory)
        # After update, item1's quantity should decrease from 10 to 8.
        updated_items = self.inventory.search_by(name=self.item1.name)
        self.assertTrue(len(updated_items) > 0)
        updated_item = updated_items[0]
        self.assertEqual(updated_item.quantity, 8)

    def test_process_payment(self):
        """Test the ShoppingCart's process_payment method."""
        self.cart.add_item(self.item1, 2)
        total_price = self.cart.calculate_total()
        result = self.cart.process_payment("dummy_payment_info", total_price)
        self.assertTrue(result)

    def test_payment_gateway_success(self):
        """Test PaymentGateway.process_payment with a valid amount."""
        result = PaymentGateway.process_payment(100.0)
        self.assertTrue(result)

    def test_payment_gateway_failure(self):
        """Test PaymentGateway.process_payment raises ValueError for non-positive amounts."""
        with self.assertRaises(ValueError):
            PaymentGateway.process_payment(0)
        with self.assertRaises(ValueError):
            PaymentGateway.process_payment(-50)

    def test_purchase_successful(self):
        """Test a successful purchase that updates inventory and clears the cart."""
        self.cart.add_item(self.item1, 2)
        # Patch validate_cart and update_inventory to use the real inventory.
        self.cart.validate_cart = lambda: ShoppingCart.validate_cart(self.cart, self.inventory)
        self.cart.update_inventory = lambda: ShoppingCart.update_inventory(self.cart, self.inventory)
        payment_gateway = PaymentGateway()
        result = self.cart.purchase(payment_gateway, "dummy_payment_info")
        self.assertTrue(result)
        self.assertEqual(len(self.cart.get_cart()), 0)
        # Verify that item1's quantity has been updated in the inventory (10 -> 8).
        updated_items = self.inventory.search_by(name=self.item1.name)
        self.assertTrue(len(updated_items) > 0)
        updated_item = updated_items[0]
        self.assertEqual(updated_item.quantity, 8)

    def test_purchase_insufficient_inventory(self):
        """Test that purchase returns False if inventory is insufficient."""
        self.cart.add_item(self.item1, 20)
        # Patch validate_cart to use real inventory.
        self.cart.validate_cart = lambda: ShoppingCart.validate_cart(self.cart, self.inventory)
        payment_gateway = PaymentGateway()
        result = self.cart.purchase(payment_gateway, "dummy_payment_info")
        self.assertFalse(result)

    def test_purchase_with_empty_cart(self):
        """Test that purchase raises an error when the cart is empty."""
        payment_gateway = PaymentGateway()
        with self.assertRaises(ValueError):
            self.cart.purchase(payment_gateway, "dummy_payment_info")

if __name__ == "__main__":
    unittest.main()
