from typing import List
from models.furniture import Furniture


# -------- Helper Func -------- #
def calc_discount(price: float, discount_percentage: float) -> float:
    """
    Calculate the discounted price for a furniture item.
    """
    if discount_percentage < 0 or discount_percentage > 100:
        raise ValueError("Discount percentage must be between 0 and 100.")
    return round(price * (1 - discount_percentage / 100), 2)


# -------- PaymentGateway CLASS -------- #
class PaymentGateway:
    """
    Simulates a payment processing system.
    """

    @staticmethod
    def process_payment(payment_info: str, total_price: float) -> bool:
        """
        Processes a payment.
        """
        if total_price <= 0:
            raise ValueError("Invalid payment amount")
        return True


# -------- ShoppingCart CLASS -------- #
class ShoppingCart:
    """
    Manages a user's shopping cart, including item addition, removal, and discount applications.
    """

    def __init__(self, user_id: str):
        """
        Initializes a shopping cart for a user.
        """
        self.user_id = user_id
        self.items: List[Furniture] = []

    def get_cart(self) -> List[Furniture]:
        """
        Retrieves the contents of the shopping cart.
        """
        return self.items

    def add_item(self, item: Furniture, quantity: int) -> bool:
        """
        Adds a Furniture item to the shopping cart.
        """
        try:
            if quantity <= 0:
                print(f"Error: Item '{item.name}' quantity is not valid.")
                return False
            for _ in range(quantity):
                self.items.append(item)
            return True
        except Exception as e:
            print(f"Error adding item to cart: {e}")
            return False

    def remove_item(self, item_name: str) -> bool:
        """
        Removes an item from the cart by name.

        Returns:
            bool: True if the item was removed, False if the item was not found or an error occurred.
        """
        try:
            # Check if the item exists in the cart
            if not any(item.name == item_name for item in self.items):
                print(f"Error: Item '{item_name}' not found in the cart.")
                return False

            # Remove the item
            self.items = [item for item in self.items if item.name != item_name]
            return True
        except Exception as e:
            print(f"Error removing item: {e}")
            return False

    def calculate_total(self) -> float:
        """
        Calculates the total cost of items in the cart.
        """
        try:
            return sum(item.price for item in self.items)
        except Exception as e:
            print(f"Error calculating total: {e}")
            return 0.0

    def apply_discount(self, discount_percentage: float) -> float:
        """
        Applies a discount to the total cart value.
        """
        try:
            total = self.calculate_total()
            return calc_discount(total, discount_percentage)
        except Exception as e:
            print(f"Error applying discount: {e}")
            return 0.0

    def validate_cart(self, inventory=None) -> bool:
        """
        Validates cart items against inventory availability.
        """
        try:
            if inventory is None:
                return True
            for item in self.items:
                found_items = inventory.search_by(item.name)
                if not found_items or found_items[0].quantity < 1:
                    return False
            return True
        except Exception as e:
            print(f"Error validating cart: {e}")
            return False

    def purchase(
        self,
        payment_gateway: PaymentGateway,
        payment_info: str,
        inventory=None,
        order_manager=None,
    ) -> bool:
        """
        Handles the purchase process, validates cart, processes payment, updates inventory, and creates an order.
        """
        try:
            if inventory is None:
                raise ValueError("Inventory instance must be provided for purchase.")
            if order_manager is None:
                raise ValueError(
                    "OrderManager instance must be provided to record the order."
                )

            total_price = self.calculate_total()
            payment_successful = payment_gateway.process_payment(
                payment_info, total_price
            )

            if payment_successful:
                order_manager.create_order(self, payment_info, total_price)
                self.update_inventory(inventory)
                self.clear_cart()
            return True
        except Exception as e:
            print(f"Error processing purchase: {e}")
            return False

    def update_inventory(self, inventory=None) -> bool:
        """
        Updates inventory after checkout.
        """
        try:
            if inventory is None:
                return False
            for item in self.items:
                if item.quantity > 0:
                    item.deduct_from_inventory(1)
                    inventory.update_quantity(item, item.quantity)
            return True
        except Exception as e:
            print(f"Error updating inventory: {e}")
            return False

    def clear_cart(self) -> bool:
        """
        Clears all items from the shopping cart.
        """
        try:
            self.items = []
            return True
        except Exception as e:
            print(f"Error clearing cart: {e}")
            return False
