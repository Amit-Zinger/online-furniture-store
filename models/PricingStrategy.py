from abc import ABC, abstractmethod

class PricingStrategy(ABC):
    @abstractmethod
    def calculate_total(self, cart):
        pass

class RegularPriceStrategy(PricingStrategy):
    def calculate_total(self, cart):
        total = 0
        for item_id, quantity in cart.items():
            item_details = cart['inventory'].get_item_details(item_id)
            total += item_details['price'] * quantity
        return total

class WelcomeDiscountStrategy(PricingStrategy):
    def calculate_total(self, cart):
        total = 0
        for item_id, quantity in cart.items():
            item_details = cart['inventory'].get_item_details(item_id)
            total += item_details['price'] * quantity
        return total * 0.9  # 10% welcome discount

class PromotionDiscountStrategy(PricingStrategy):
    def calculate_total(self, cart):
        total = 0
        for item_id, quantity in cart.items():
            item_details = cart['inventory'].get_item_details(item_id)
            total += item_details['price'] * quantity
        return total * 0.8  # 20% promotion discount

class DiscountPriceStrategy(PricingStrategy):
    def calculate_total(self, cart):
        total = 0
        for item_id, quantity in cart.items():
            item_details = cart['inventory'].get_item_details(item_id)
            if 'discount_price' in item_details:
                total += item_details['discount_price'] * quantity
            else:
                total += item_details['price'] * quantity
        return total

class PricingContext:
    def __init__(self, strategy: PricingStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: PricingStrategy):
        self.strategy = strategy

    def execute_strategy(self, cart):
        return self.strategy.calculate_total(cart)
