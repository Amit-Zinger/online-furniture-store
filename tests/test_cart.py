import unittest
from models.cart import ShoppingCart
from models.furniture import Furniture
from models.cart import PaymentGateway
from app.utils import calc_discount


class TestShoppingCart(unittest.TestCase):

    def setUp(self):
        """This method is run before each test."""
        self.cart = ShoppingCart("user123")
        self.item1 = Furniture(name="Chair", price=100.0)
        self.item2 = Furniture(name="Table", price=200.0)

    def test_add_item(self):
        """Test adding items to the cart."""
        self.cart.add_item(self.item1, 2)
        self.assertEqual(len(self.cart.get_cart()), 1)
        self.assertEqual(self.cart.get_cart()[0]['item'], self.item1)
        self.assertEqual(self.cart.get_cart()[0]['quantity'], 2)

    def test_calculate_total(self):
        """Test the total price calculation."""
        self.cart.add_item(self.item1, 2)
        self.cart.add_item(self.item2, 1)
        self.assertEqual(self.cart.calculate_total(), 400.0)

    def test_apply_discount(self):
        """Test applying a discount to the cart."""
        self.cart.add_item(self.item1, 2)
        self.cart.add_item(self.item2, 1)
        discounted_total = self.cart.apply_discount(10)  # 10% discount
        self.assertEqual(discounted_total, 360.0)  # (100*2 + 200) * 0.9

    def test_clear_cart(self):
        """Test clearing the cart."""
        self.cart.add_item(self.item1, 2)
        self.cart.add_item(self.item2, 1)
        self.cart.clear_cart()
        self.assertEqual(len(self.cart.get_cart()), 0)

    def test_purchase_successful(self):
        """Test successful purchase with enough inventory."""
        self.cart.add_item(self.item1, 2)
        self.cart.add_item(self.item2, 1)

        # Mock the payment gateway
        payment_gateway = PaymentGateway()
        result = self.cart.purchase(payment_gateway)
        self.assertTrue(result)

        # Verify that the inventory has been updated (mocked in this example)
        self.assertEqual(self.item1.quantity, 8)  # Assuming initial quantity was 10
        self.assertEqual(self.item2.quantity, 9)  # Assuming initial quantity was 10

    def test_purchase_insufficient_inventory(self):
        """Test purchase when inventory is insufficient."""
        self.cart.add_item(self.item1, 20)  # Try to buy more than the stock
        payment_gateway = PaymentGateway()
        with self.assertRaises(ValueError):
            self.cart.purchase(payment_gateway)

    def test_process_payment(self):
        """Test the payment processing functionality."""
        payment_gateway = PaymentGateway()

        # In a real scenario, you would mock the external payment API
        with self.assertLogs(level="INFO") as log:
            self.cart.purchase(payment_gateway)
            self.assertIn("Processing payment of $400.0", log.output)


if __name__ == '__main__':
    unittest.main()
