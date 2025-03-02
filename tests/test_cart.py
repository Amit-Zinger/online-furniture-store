import unittest
from unittest.mock import MagicMock
from models.cart import ShoppingCart, PaymentGateway
from app.utils import calc_discount


# Mock Item class for testing
class MockItem:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity


class TestShoppingCart(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart(user_id="user123")
        self.item1 = MockItem("Table", 100, 10)
        self.item2 = MockItem("Chair", 50, 20)
        self.payment_gateway = PaymentGateway()
        self.inventory = MagicMock()
        self.order_manager = MagicMock()

    def test_add_item(self):
        self.cart.add_item(self.item1, 2)
        self.assertEqual(len(self.cart.get_cart()), 1)
        self.assertEqual(self.cart.get_cart()[0]['quantity'], 2)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.cart.add_item(self.item1, 0)

    def test_remove_item(self):
        self.cart.add_item(self.item1, 2)
        self.cart.add_item(self.item2, 3)
        self.cart.remove_item("Table")
        self.assertEqual(len(self.cart.get_cart()), 1)
        self.assertEqual(self.cart.get_cart()[0]['item'].name, "Chair")

    def test_clear_cart(self):
        self.cart.add_item(self.item1, 2)
        self.cart.clear_cart()
        self.assertEqual(len(self.cart.get_cart()), 0)

    def test_calculate_total(self):
        self.cart.add_item(self.item1, 2)
        self.cart.add_item(self.item2, 3)
        self.assertEqual(self.cart.calculate_total(), 350)

    def test_apply_discount(self):
        self.cart.add_item(self.item1, 2)
        self.cart.add_item(self.item2, 3)
        self.assertEqual(self.cart.apply_discount(10), calc_discount(350, 10))

    def test_validate_cart_no_inventory(self):
        self.assertTrue(self.cart.validate_cart())

    def test_validate_cart_with_inventory(self):
        self.inventory.search_by.side_effect = lambda name: [MockItem(name, 100, 10)]
        self.cart.add_item(self.item1, 2)
        self.assertTrue(self.cart.validate_cart(self.inventory))

    def test_validate_cart_insufficient_stock(self):
        self.inventory.search_by.side_effect = lambda name: [MockItem(name, 100, 1)]
        self.cart.add_item(self.item1, 2)
        self.assertFalse(self.cart.validate_cart(self.inventory))

    def test_purchase_successful(self):
        self.cart.add_item(self.item1, 2)
        self.payment_gateway.process_payment = MagicMock(return_value=True)
        self.cart.purchase(self.payment_gateway, "card123", self.inventory, self.order_manager)
        self.assertEqual(len(self.cart.get_cart()), 0)
        self.order_manager.create_order.assert_called()
        self.inventory.update_quantity.assert_called()

    def test_purchase_fails_due_to_payment(self):
        self.cart.add_item(self.item1, 2)
        self.payment_gateway.process_payment = MagicMock(return_value=False)
        self.cart.purchase(self.payment_gateway, "card123", self.inventory, self.order_manager)
        self.assertNotEqual(len(self.cart.get_cart()), 0)
        self.order_manager.create_order.assert_not_called()

    def test_purchase_without_inventory_or_order_manager(self):
        self.cart.add_item(self.item1, 2)
        with self.assertRaises(ValueError):
            self.cart.purchase(self.payment_gateway, "card123", None, self.order_manager)
        with self.assertRaises(ValueError):
            self.cart.purchase(self.payment_gateway, "card123", self.inventory, None)


if __name__ == "__main__":
    unittest.main()
