from app.utils import calc_discount


class PaymentGateway:
    @staticmethod
    def process_payment(amount):
        print(f"Processing payment of ${amount}")
        # Here you can implement actual payment logic (e.g., via Stripe, PayPal)
        pass


class ShoppingCart:
    def __init__(self, user_id):
        self.user_id = user_id
        self.items = []

    def get_cart(self):
        return self.items

    def add_item(self, item, quantity):
        self.items.append({"item": item, "quantity": quantity})

    def clear_cart(self):
        self.items = []

    def calculate_total(self):
        """Calculate the total price of the cart."""
        return sum(item['item'].price * item['quantity'] for item in self.items)

    def apply_discount(self, discount_percentage):
        """Apply a percentage discount to the total cart price using calc_discount."""
        total = self.calculate_total()
        return calc_discount(total, discount_percentage)

    def purchase(self, payment_gateway):
        total = self.calculate_total()
        if total == 0:
            raise ValueError("Cart is empty")
        payment_gateway.process_payment(total)
        for item in self.items:
            item['item'].deduct_from_inventory(item['quantity'])
        return True


