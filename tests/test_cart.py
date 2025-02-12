import unittest
from models.cart import ShoppingCart, PaymentGateway
from models.furniture import Chair


class TestShoppingCart(unittest.TestCase):

    def setUp(self):
        """Set up a shopping cart instance before each test."""
        self.cart = ShoppingCart("user123")
        self.item1 = Chair(name="Office Chair", description="Ergonomic chair", price=150.0, dimensions="50x50x100cm",
                           serial_number="CH001", quantity=10, weight=10, manufacturing_country="Germany", has_wheels=True, how_many_legs=5)
        self.item2 = Chair(name="Gaming Chair", description="Comfortable gaming chair", price=200.0, dimensions="55x55x110cm",
                           serial_number="CH002", quantity=5, weight=12, manufacturing_country="USA", has_wheels=True, how_many_legs=5)

    def test_add_item(self):
        """Test adding items to the cart."""
        self.cart.add_item(self.item1, 2)
        self.assertEqual(len(self.cart.get_cart()), 1)
        self.assertEqual(self.cart.get_cart()[0]['quantity'], 2)

    def test_remove_item(self):
        """Test removing an item from the cart."""
        self.cart.add_item(self.item1, 1)
        self.cart.remove_item(self.item1.name)
        self.assertEqual(len(self.cart.get_cart()), 0)

    def test_calculate_total(self):
        """Test total price calculation of the cart."""
        self.cart.add_item(self.item1, 2)
        self.cart.add_item(self.item2, 1)
        self.assertEqual(self.cart.calculate_total(), 500.0)

    def test_apply_discount(self):
        """Test applying a discount to the cart."""
        self.cart.add_item(self.item1, 2)
        discounted_total = self.cart.apply_discount(10)  # 10% discount
        self.assertEqual(discounted_total, 270.0)  # (150*2) * 0.9

    def test_clear_cart(self):
        """Test clearing the cart."""
        self.cart.add_item(self.item1, 2)
        self.cart.clear_cart()
        self.assertEqual(len(self.cart.get_cart()), 0)

    def test_purchase_successful(self):
        """Test successful purchase and inventory update."""
        self.cart.add_item(self.item1, 2)
        payment_gateway = PaymentGateway()
        result = self.cart.purchase(payment_gateway)
        self.assertTrue(result)
        self.assertEqual(self.item1.quantity, 8)

    def test_purchase_insufficient_inventory(self):
        """Test purchase fails if inventory is insufficient."""
        self.cart.add_item(self.item1, 20)
        payment_gateway = PaymentGateway()
        with self.assertRaises(ValueError):
            self.cart.purchase(payment_gateway)

if __name__ == '__main__':
    unittest.main()
