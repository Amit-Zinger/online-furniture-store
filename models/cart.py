from typing import List, Dict


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

    discounted_price = price * (1 - discount_percentage / 100)
    return round(discounted_price, 2)


class PaymentGateway:
    """
    Simulates a payment processing system.
    Can be integrated with a real API in the future.
    """

    @staticmethod
    def process_payment(payment_info: str, total_price: float) -> bool:
        """
        Processes a payment.

        Args:
            payment_info (str): Payment details.
            total_price (float): The total amount to be charged.

        Returns:
            bool: True if payment is successful; raises ValueError if the amount is invalid.
        """
        if total_price <= 0:
            raise ValueError("❌ Invalid payment amount")
        print(f"💳 Processing payment of ${total_price}")
        return True  # Always succeeds for mock payments


class ShoppingCart:
    """
    Manages a user's shopping cart, including item addition, removal, and discount applications.

    Attributes:
        user_id (str): Unique identifier for the user.
        items (List[Dict]): List of items in the cart, each containing item details and quantity.
    """

    def __init__(self, user_id: str):
        """
        Initializes a shopping cart for a user.

        Args:
            user_id (str): The unique identifier of the user.
        """
        self.user_id = user_id
        self.items: List[Dict] = []

    def get_cart(self) -> List[Dict]:
        """
        Retrieves the contents of the shopping cart.

        Returns:
            List[Dict]: A list containing items and their quantities.
        """
        return self.items

    def add_item(self, item, quantity: int) -> None:
        """
        Adds an item to the shopping cart.

        Args:
            item: The item object to be added.
            quantity (int): The number of items to add.

        Raises:
            ValueError: If the quantity is less than or equal to 0.
        """
        if quantity <= 0:
            raise ValueError("❌ Quantity must be greater than 0")
        self.items.append({"item": item, "quantity": quantity})
        print(f"🛒 Added {quantity} of {item.name} to cart.")

    def remove_item(self, item_name: str) -> None:
        """
        Removes an item from the cart by name.

        Args:
            item_name (str): The name of the item to remove.
        """
        self.items = [item for item in self.items if item["item"].name != item_name]
        print(f"🗑 Removed {item_name} from cart.")

    def clear_cart(self) -> None:
        """
        Clears all items from the shopping cart.
        """
        self.items = []
        print("🛒 Cart has been cleared.")

    def calculate_total(self) -> float:
        """
        Calculates the total cost of items in the cart.

        Returns:
            float: The total price of all items in the cart.
        """
        return sum(item["item"].price * item["quantity"] for item in self.items)

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

        If an inventory object is provided, performs detailed validation.
        Otherwise, performs a default validation.

        Args:
            inventory: (Optional) Inventory system to validate against.

        Returns:
            bool: True if all items are available, otherwise False.
        """
        if inventory is None:
            print("🔍 Validating cart with inventory system (default validation)...")
            return True
        for item_dic in self.items:
            quantity = item_dic["quantity"]
            found_items = inventory.search_by(item_dic["item"].name)
            if not found_items:
                print(f"⚠️ Item {item_dic['item'].name} isn't available. Validation failed.")
                return False
            found_item = found_items[0]
            if found_item.quantity < quantity:
                print(f"⚠️ Item {found_item.name} quantity is {found_item.quantity}, validation failed.")
                return False
        return True

    def purchase(self, payment_gateway: PaymentGateway, payment_info: str, inventory=None, order_manager=None):
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
        print("✅ Starting checkout process...")

        # Ensure required dependencies are provided
        if inventory is None:
            raise ValueError("❌ Inventory instance must be provided for purchase.")

        if order_manager is None:
            raise ValueError("❌ OrderManager instance must be provided to record the order.")

        # Calculate total price
        total_price = self.calculate_total()

        # ✅ Call the `process_payment` method correctly
        payment_successful = payment_gateway.process_payment(payment_info, total_price)

        if payment_successful:
            print("✅ Payment successful. Creating order...")

            # Create an order
            order_manager.create_order(self, payment_info, total_price)

            # ✅ Update inventory stock
            self.update_inventory(inventory)

            # ✅ Clear cart after successful purchase
            self.clear_cart()

            print("✅ Checkout process completed successfully.")
        else:
            print("❌ Payment failed. Purchase was not completed.")

    def update_inventory(self, inventory=None) -> None:
        """
        Updates inventory after checkout.

        Args:
            inventory: (Optional) Inventory system to update. If None, skips update.
        """
        if inventory is None:
            print("⚠️ No inventory provided; skipping inventory update.")
            return
        for item_dic in self.items:
            item_obj = item_dic["item"]
            requested_quantity = item_dic["quantity"]
            new_quantity = item_obj.quantity - requested_quantity
            inventory.update_quantity(item_obj, new_quantity)
