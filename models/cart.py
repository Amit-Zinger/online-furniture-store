from app.utils import calc_discount
from app.utils import calc_discount


class PaymentGateway:
    """
    מחלקה המדמה תהליך תשלום, ניתן לשלב בה API אמיתי בעתיד.
    """

    @staticmethod
    def process_payment(amount):
        if amount <= 0:
            raise ValueError("Invalid payment amount")
        print(f"Processing payment of ${amount}")
        return True


class ShoppingCart:
    """
    עגלת קניות למשתמש, ניהול הוספה, הסרה, והנחות.
    """

    def __init__(self, user_id):
        self.user_id = user_id
        self.items = []

    def get_cart(self):
        return self.items

    def add_item(self, item, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        self.items.append({"item": item, "quantity": quantity})
        print(f"Added {quantity} of {item.name} to cart.")

    def remove_item(self, item_name):
        """מסיר פריט לפי שם מהעגלה."""
        self.items = [
            item for item in self.items if item["item"].name != item_name]
        print(f"Removed {item_name} from cart.")

    def clear_cart(self):
        """מאפס את העגלה לחלוטין."""
        self.items = []
        print("Cart has been cleared.")

    def calculate_total(self):
        """חישוב הסכום הכולל של הפריטים בעגלה."""
        return sum(item["item"].price * item["quantity"]
                   for item in self.items)

    def apply_discount(self, discount_percentage):
        """החלת הנחה כללית על העגלה."""
        total = self.calculate_total()
        return calc_discount(total, discount_percentage)

    def purchase(self, payment_gateway):
        """סיום הקנייה וניקוי העגלה לאחר תשלום מוצלח."""
        total = self.calculate_total()
        if total == 0:
            raise ValueError("Cart is empty")

        if payment_gateway.process_payment(total):
            for item in self.items:
                item["item"].deduct_from_inventory(item["quantity"])
            self.clear_cart()
            print("Purchase successful!")
            return True
        return False
