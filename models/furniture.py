from abc import ABC
from typing import List
from app.utils import calc_discount


class Furniture(ABC):
    """
    Abstract class representing a piece of furniture.
    """

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        dimensions: str,
        serial_number: str,
        quantity: int,
        weight: float,
        manufacturing_country: str,
        interested_clients: List[str] = None,
    ):
        self._validate_positive_value(price, "Price")
        self._validate_positive_value(weight, "Weight")
        self._validate_positive_value(quantity, "Quantity")

        self.name = name
        self.description = description
        self.price = price
        self.dimensions = dimensions
        self.serial_number = serial_number
        self.quantity = quantity
        self.weight = weight
        self.manufacturing_country = manufacturing_country
        self.interested_clients = interested_clients if interested_clients else []
        self.tax_rate = 0.17  # Default tax rate

    def __str__(self):
        return f"{self.name} - {self.description} | Price: ${self.get_final_price()} | Stock: {self.quantity}"

    def deduct_from_inventory(self, quantity):
        """
        Deducts a specified quantity from the inventory.

        :param quantity: The number of items to deduct.
        :raises ValueError: If there is not enough stock.
        """
        if self.quantity < quantity:
            raise ValueError(f"Not enough stock for {self.name}")
        self.quantity -= quantity

    def is_out_of_stock(self) -> bool:
        """
        Checks if the item is out of stock.

        :return: True if quantity is 0, otherwise False.
        """
        return self.quantity == 0

    def apply_discount(self, discount_percentage: float):
        """
        Apply a discount to the price of the furniture.

        :param discount_percentage: The percentage discount to apply.
        :raises ValueError: If discount is not between 0 and 100.
        """
        if not (0 <= discount_percentage <= 100):
            raise ValueError("Discount percentage must be between 0 and 100.")

        self.price = self._calculate_discounted_price(discount_percentage)

    def apply_tax(self, tax_rate: float = None):
        """
        Apply tax to the price of the furniture.

        :param tax_rate: The tax rate to apply (default is 17%).
        :raises ValueError: If tax rate is negative.
        """
        if tax_rate is not None:
            self._validate_positive_value(tax_rate, "Tax rate")
            self.tax_rate = tax_rate

    def get_final_price(self) -> float:
        """
        Calculate the final price of the furniture after tax.

        :return: Price after tax.
        """
        return round(self.price * (1 + self.tax_rate), 2)

    def _calculate_discounted_price(self, discount_percentage: float) -> float:
        """
        Internal helper function to calculate price after discount.

        :param discount_percentage: The discount percentage to apply.
        :return: Discounted price.
        """
        return calc_discount(self.price, discount_percentage)

    def _validate_positive_value(self, value, field_name):
        """
        Helper function to validate that a value is positive.

        :param value: The value to check.
        :param field_name: The name of the field being validated.
        :raises ValueError: If value is not positive.
        """
        if value <= 0:
            raise ValueError(f"{field_name} must be a positive value.")


class Chair(Furniture):
    def __init__(self, has_wheels: bool, how_many_legs: int, **kwargs):
        super().__init__(**kwargs)
        self.has_wheels = has_wheels
        self.how_many_legs = how_many_legs


class Sofa(Furniture):
    def __init__(self, how_many_seats: int, can_turn_to_bed: bool, **kwargs):
        super().__init__(**kwargs)
        self.how_many_seats = how_many_seats
        self.can_turn_to_bed = can_turn_to_bed


class Bed(Furniture):
    def __init__(self, has_storage: bool, has_back: bool, **kwargs):
        super().__init__(**kwargs)
        self.has_storage = has_storage
        self.has_back = has_back


class Table(Furniture):
    def __init__(self, expandable: bool, how_many_seats: int, is_foldable: bool, **kwargs):
        super().__init__(**kwargs)
        self.expandable = expandable
        self.how_many_seats = how_many_seats
        self.is_foldable = is_foldable


class Closet(Furniture):
    def __init__(self, has_mirrors: bool, number_of_shelves: int, how_many_doors: int, **kwargs):
        super().__init__(**kwargs)
        self.has_mirrors = has_mirrors
        self.number_of_shelves = number_of_shelves
        self.how_many_doors = how_many_doors
