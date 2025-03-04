from typing import List
from models.furniture import Furniture


def calc_discount(price: float, discount_percentage: float) -> float:
    """
    Calculate the discounted price for a furniture item.

    Parameters:
    price (float): The original price of the item.
    discount_percentage (float): The percentage discount to apply.

    Returns:
    float: The discounted price.
    """
    if discount_percentage < 0 or discount_percentage > 100:
        raise ValueError("Discount percentage must be between 0 and 100.")

    return round(price * (1 - discount_percentage / 100), 2)


class PaymentGateway:
    """
    Simulates a payment processing system.
    """

    @staticmethod
    def process_payment(payment_info: str, total_price: float) -> bool:
        """
        Processes a payment.

        Args:
            payment_info (str): Payment details.
            total_price (float): The total amount to be charged.

        Returns:
            bool: True if payment is successful, raises ValueError if the amount is invalid.
        """
        if total_price <= 0:
            raise ValueError("Invalid payment amount")

        return True


class ShoppingCart:
    """
    Manages a user's shopping cart, including item addition, removal, and discount applications.
    """

    def __init__(self, user_id: str):
        """
        Initializes a shopping cart for a user.

        Args:
            user_id (str): The unique identifier of the user.
        """
        self.user_id = user_id
        self.items: List[Furniture] = []

    def get_cart(self) -> List[Furniture]:
        """
        Retrieves the contents of the shopping cart.

        Returns:
            List[Furniture]: A list of Furniture objects in the cart.
        """
        return self.items

    def add_item(self, item: Furniture, quantity: int) -> bool:
        """
        Adds a Furniture item to the shopping cart.

        Args:
            item (Furniture): The Furniture object to be added.
            quantity (int): The number of items to add.

        Raises:
            ValueError: If the quantity is less than or equal to 0.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        for _ in range(quantity):
            self.items.append(item)

        return True

    def remove_item(self, item_name: str) -> bool:
        """
        Removes an item from the cart by name.

        Args:
            item_name (str): The name of the item to remove.
        """
        self.items = [item for item in self.items if item.name != item_name]

        return True
    def calculate_total(self) -> float:
        """
        Calculates the total cost of items in the cart.

        Returns:
            float: The total price of all items in the cart.
        """
        return sum(item.price for item in self.items)

    def apply_discount(self, discount_percentage: float) -> float:
        """
        Applies a discount to the total cart value.

        Args:
            discount_percentage (float): The discount percentage to be applied.

        Returns:
            float: The total price after applying the discount.
        """
        total = self.calculate_total()
        return calc_discount(total, discount_percentage)

    def validate_cart(self, inventory=None) -> bool:
        """
        Validates cart items against inventory availability.

        Args:
            inventory: (Optional) Inventory system to validate against.

        Returns:
            bool: True if all items are available, otherwise False.
        """
        if inventory is None:
            return True

        for item in self.items:
            found_items = inventory.search_by(item.name)
            if not found_items or found_items[0].quantity < 1:
                return False
        return True

    def purchase(self, payment_gateway: PaymentGateway, payment_info: str, inventory=None, order_manager=None) -> bool:
        """
        Handles the purchase process, validates cart, processes payment, updates inventory, and creates an order.

        Args:
            payment_gateway (PaymentGateway): Instance of PaymentGateway to process payment.
            payment_info (str): Payment details.
            inventory (Inventory): Inventory instance for stock management.
            order_manager (OrderManager): OrderManager instance to store orders.

        Raises:
            ValueError: If inventory or order_manager is not provided.
        """
        if inventory is None:
            raise ValueError("Inventory instance must be provided for purchase.")
        if order_manager is None:
            raise ValueError("OrderManager instance must be provided to record the order.")

        total_price = self.calculate_total()
        payment_successful = payment_gateway.process_payment(payment_info, total_price)

        if payment_successful:
            order_manager.create_order(self, payment_info, total_price)
            self.update_inventory(inventory)
            self.clear_cart()

        return True

    def update_inventory(self, inventory=None) -> bool:
        """
        Updates inventory after checkout.

        Args:
            inventory: (Optional) Inventory system to update. If None, skips update.
        """
        if inventory is None:
            return

        for item in self.items:
            if item.quantity > 0:
                item.deduct_from_inventory(1)
                inventory.update_quantity(item, item.quantity)

        return True

    def clear_cart(self) -> bool:
        """
        Clears all items from the shopping cart.
        """
        self.items = []

        return True