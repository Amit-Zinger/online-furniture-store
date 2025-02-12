class ShoppingCart:
    def __init__(self, user_id):
        self.user_id = user_id
        self.items = []

    def get_cart(self):
        pass

    def add_item(self, item, quantity):
        pass

    def clear_cart(self):
        pass

    def calculate_total(self):
        pass

    def purchase(self, payment_gateway):
        for item in self.items:
            if item.quantity > item.inventory:
                raise ValueError
            item.deduct_from_invetory(item.quanity)


class PaymentGateway:
    @staticmethod
    def process_payment(amount):
        pass



