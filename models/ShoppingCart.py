from PricingStrategy import (
    PricingContext,
    PricingStrategy,
    RegularPriceStrategy,
)
from OrderManager import OrderManager


class ShoppingCart:
    def __init__(self, client_id, inventory, pricing_strategy=None):
        self.client_id = client_id
        self.inventory = inventory
        # Default to RegularPriceStrategy if no strategy is provided
        self.pricing_strategy = pricing_strategy or RegularPriceStrategy()
        self.cart = {}

    def add(self, item_id, quantity):
        if self.inventory.get_available_quantity(item_id) < quantity:
            print(f"Insufficient stock for item {item_id}.")
            return

        self.cart[item_id] = self.cart.get(item_id, 0) + quantity
        print(f"Added {quantity} of item {item_id} to the cart.")

    def clear_shopping_cart(self):
        self.cart.clear()
        print("Shopping cart cleared.")

    def remove(self, item_id):
        if item_id in self.cart:
            del self.cart[item_id]
            print(f"Item {item_id} removed from the cart.")
        else:
            print(f"Item {item_id} not found in the cart.")

    def view_cart(self):
        if not self.cart:
            print("The shopping cart is empty.")
        else:
            print("Current items in the cart:")
            for item_id, quantity in self.cart.items():
                item_details = self.inventory.get_item_details(item_id)
                print(
                    f"Item ID: {item_id}, Name: {item_details['name']}, "
                    f"Quantity: {quantity}, Price: {item_details['price']}"
                )

    def validate_cart(self):
        unavailable_items = [
            item_id
            for item_id, quantity in self.cart.items()
            if self.inventory.get_available_quantity(item_id) < quantity
        ]
        if unavailable_items:
            print(f"The following items are unavailable: {unavailable_items}")
            return False
        print("All items in the cart are available.")
        return True

    def checkout(self, payment_info):
        print("Starting checkout process...")
        if not self.validate_cart():
            print("Checkout failed: Some items are unavailable.")
            return False

        # Calculate total price using PricingContext
        pricing_context = PricingContext(self.pricing_strategy)
        total_price = pricing_context.execute_strategy(
            {"cart": self.cart, "inventory": self.inventory}
        )

        if not self.process_payment(payment_info, total_price):
            print("Checkout failed: Payment processing error.")
            return False

        print("Payment successful. Creating order...")
        order_manager = OrderManager()
        order_manager.create_order(self, payment_info, total_price)

        print("Updating inventory...")
        self.inventory.update_inventory(self.cart)

        self.clear_shopping_cart()
        print("Checkout process completed successfully.")
        return True

    def process_payment(self, payment_info, total_price):
        print(f"Processing payment of {total_price} for client {self.client_id}...")
        return True  # Mock success
