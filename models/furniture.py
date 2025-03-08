from abc import ABC
from typing import Optional


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
        self.tax_rate = 0.17  # Default tax rate

    @property
    def item_desc(self) -> str:
        return f"{self.name} - {self.description} | Price: ${self.price} | Stock: {self.quantity}"

    def deduct_from_inventory(self, quantity):
        """
        Deducts a specified quantity from the inventory.

        :param quantity: The number of items to deduct.
        :raises ValueError: If there is not enough stock.
        """
        if self.quantity < quantity:
            raise ValueError(f"Not enough stock for {self.name}")
        self.quantity -= quantity

    def is_available(self, min_stock: int = 1) -> bool:
        return self.quantity >= min_stock

    def apply_discount(self, discount_percentage: float) -> float:
        if discount_percentage < 0 or discount_percentage > 100:
            raise ValueError("Discount percentage must be between 0 and 100.")
        self.price = round(self.price * (1 - discount_percentage / 100), 2)
        return self.price

    def apply_tax(self, tax_rate: Optional[float] = None) -> None:
        if tax_rate is not None:
            self._validate_positive_value(tax_rate, "Tax rate")
            self.tax_rate = tax_rate
        self.price = round(self.price * (1 + self.tax_rate), 2)

    @staticmethod
    def _validate_positive_value(value, field_name):
        """
        Helper function to validate that a value is positive.

        :param value: The value to check.
        :param field_name: The name of the field being validated.
        :raises ValueError: If value is not positive.
        """
        if value <= 0:
            raise ValueError(f"{field_name} must be a positive value.")


class Chair(Furniture):
    def __init__(
        self, has_wheels: bool = False, how_many_legs: int = 4, **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.has_wheels = has_wheels
        self.how_many_legs = how_many_legs


class Sofa(Furniture):
    def __init__(
        self, how_many_seats: int = 3, can_turn_to_bed: bool = False, **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.how_many_seats = how_many_seats
        self.can_turn_to_bed = can_turn_to_bed


class Bed(Furniture):
    def __init__(
        self, has_storage: bool = False, has_back: bool = False, **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.has_storage = has_storage
        self.has_back = has_back


class Table(Furniture):
    def __init__(
        self,
        expandable: bool = False,
        how_many_seats: int = 4,
        can_fold: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.expandable = expandable
        self.how_many_seats = how_many_seats
        self.can_fold = can_fold


class Closet(Furniture):
    def __init__(
        self,
        has_mirrors: bool = False,
        number_of_shelves: int = 3,
        how_many_doors: int = 2,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.has_mirrors = has_mirrors
        self.number_of_shelves = number_of_shelves
        self.how_many_doors = how_many_doors
