import unittest
from unittest.mock import MagicMock
from models.cart import ShoppingCart, PaymentGateway
from models.cart import calc_discount
from models.furniture import Chair, Table


class TestShoppingCart(unittest.TestCase):
    """
    Unit tests for the ShoppingCart class.
    """

    def setUp(self):
        """
        Initializes the test case setup.
        """
        self.cart = ShoppingCart(user_id="user123")
        self.item1 = Table(
            name="Dining Table",
            description="Wooden table",
            price=100,
            dimensions="100x50",
            serial_number="T123",
            quantity=10,
            weight=20,
            manufacturing_country="USA",
        )
        self.item2 = Chair(
            name="Office Chair",
            description="Ergonomic chair",
            price=50,
            dimensions="40x40",
            serial_number="C123",
            quantity=20,
            weight=10,
            manufacturing_country="Germany",
            has_wheels=True,
        )
        self.payment_gateway = PaymentGateway()
        self.inventory = MagicMock()
        self.order_manager = MagicMock()


    def test_add_invalid_quantity(self) -> None:
        """
        Test that adding an item with invalid quantity return False.
        """
        assert self.cart.add_item(self.item1, -1) is False

    def test_remove_non_existent_item(self) -> None:
        """
        Test removing an item that does not exist in the cart.
        """
        result = self.cart.remove_item("NonExistentItem")
        self.assertFalse(result, "Removing a non-existent item should return False.")

    def test_calculate_total_with_empty_cart(self) -> None:
        """
        Test calculating total price when the cart is empty.
        """
        self.assertEqual(self.cart.calculate_total(), 0.0, "Total should be 0 for an empty cart.")

    def test_apply_discount_invalid_percentage(self) -> None:
        """
        Test that applying an invalid discount percentage raises an exception.
        """
        with self.assertRaises(ValueError):
            calc_discount(100, 150)  # Discount greater than 100%

    def test_payment_with_invalid_amount(self) -> None:
        """
        Test that attempting to process payment with an invalid amount raises an exception.
        """
        with self.assertRaises(ValueError):
            self.payment_gateway.process_payment("card123", -50)

    def test_purchase_without_inventory(self) -> None:
        """
        Test attempting a purchase without providing inventory, which should raise an error.
        """
        result = self.cart.purchase(self.payment_gateway, "card123", None, self.order_manager)
        self.assertFalse(result, "Purchase should fail if inventory is not provided.")

    def test_purchase_without_order_manager(self) -> None:
        """
        Test attempting a purchase without providing an order manager, which should raise an error.
        """
        result = self.cart.purchase(self.payment_gateway, "card123", self.inventory, None)
        self.assertFalse(result, "Purchase should fail if order manager is not provided.")

    def test_add_item(self):
        """
        Tests adding an item to the shopping cart.
        """
        self.cart.add_item(self.item1, 2)
        self.assertEqual(len(self.cart.get_cart()), 2)

    def test_remove_item(self):
        """
        Tests removing an item from the shopping cart.
        """
        self.cart.add_item(self.item1, 2)
        self.cart.add_item(self.item2, 3)
        self.cart.remove_item("Dining Table")
        self.assertEqual(len(self.cart.get_cart()), 3)

    def test_validate_cart_with_inventory(self):
        """
        Tests validating the cart with inventory availability.
        """
        self.inventory.search_by.side_effect = lambda name: (
            [self.item1] if name == "Dining Table" else [self.item2]
        )
        self.cart.add_item(self.item1, 2)
        self.assertTrue(self.cart.validate_cart(self.inventory))

    def test_calculate_total(self):
        """
        Tests calculating the total price of items in the cart.
        """
        self.cart.add_item(self.item1, 2)
        self.cart.add_item(self.item2, 3)
        self.assertEqual(self.cart.calculate_total(), 350)

    def test_apply_discount(self):
        """
        Tests applying a discount to the total cart value.
        """
        self.cart.add_item(self.item1, 2)
        self.cart.add_item(self.item2, 3)
        self.assertEqual(self.cart.apply_discount(10), calc_discount(350, 10))

    def test_purchase_successful(self):
        """
        Tests a successful purchase process.
        """
        self.cart.add_item(self.item1, 2)
        self.payment_gateway.process_payment = MagicMock(return_value=True)
        self.cart.purchase(
            self.payment_gateway, "card123", self.inventory, self.order_manager
        )
        self.assertEqual(len(self.cart.get_cart()), 0)
        self.order_manager.create_order.assert_called()
        self.inventory.update_quantity.assert_called()

    def test_purchase_fails_due_to_payment(self):
        """
        Tests a failed purchase due to payment failure.
        """
        self.cart.add_item(self.item1, 2)
        self.payment_gateway.process_payment = MagicMock(return_value=False)
        self.cart.purchase(
            self.payment_gateway, "card123", self.inventory, self.order_manager
        )
        self.assertNotEqual(len(self.cart.get_cart()), 0)
        self.order_manager.create_order.assert_not_called()

    def test_purchase_without_inventory_or_order_manager(self):
        """
        Tests attempting a purchase without inventory or order manager.
        """
        self.cart.add_item(self.item1, 2)

        # Instead of expecting ValueError, expect False return value
        result_no_inventory = self.cart.purchase(
            self.payment_gateway, "card123", None, self.order_manager
        )
        result_no_order_manager = self.cart.purchase(
            self.payment_gateway, "card123", self.inventory, None
        )

        self.assertFalse(result_no_inventory)
        self.assertFalse(result_no_order_manager)


if __name__ == "__main__":
    unittest.main()
