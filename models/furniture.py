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
        if price <= 0:
            raise ValueError("Price must be a positive value.")
        if weight <= 0:
            raise ValueError("Weight must be a positive value.")
        if quantity <= 0:
            raise ValueError("Quantity must be a positive value.")

        self.name = name
        self.description = description
        self.price = price
        self.dimensions = dimensions
        self.serial_number = serial_number
        self.quantity = quantity
        self.weight = weight
        self.manufacturing_country = manufacturing_country
        self.interested_clients = interested_clients if interested_clients else []

    def __str__(self):
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
        """
        new_price = calc_discount(self.price, discount_percentage)
        if new_price > 0:
            self.price = new_price

    def apply_tax(self, tax_rate=0.17):
        """
        Apply tax to the price of the furniture.

        param tax_rate: The tax rate to apply (default is 17%).
        """
        self.price += self.price * tax_rate

    def is_valid_price(self) -> bool:
        """Validate if the price is a positive number."""
        return self.price > 0

    def get_description(self) -> str:
        """Returns a description of the furniture."""
        return self.description


class Chair(Furniture):
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
            has_wheels: bool,
            how_many_legs: int,
            interested_clients: List[str] = None,
    ):
        super().__init__(
            name, description, price, dimensions, serial_number,
            quantity, weight, manufacturing_country, interested_clients,
        )
        self.has_wheels = has_wheels
        self.how_many_legs = how_many_legs


class Sofa(Furniture):
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
            how_many_seats: int,
            can_turn_to_bed: bool,
            interested_clients: List[str] = None,
    ):
        super().__init__(
            name, description, price, dimensions, serial_number,
            quantity, weight, manufacturing_country, interested_clients,
        )
        self.how_many_seats = how_many_seats
        self.can_turn_to_bed = can_turn_to_bed


class Bed(Furniture):
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
            has_storage: bool,
            has_back: bool,
            interested_clients: List[str] = None,
    ):
        super().__init__(
            name, description, price, dimensions, serial_number,
            quantity, weight, manufacturing_country, interested_clients,
        )
        self.has_storage = has_storage
        self.has_back = has_back


class Table(Furniture):
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
            expandable: bool,
            how_many_seats: int,
            is_foldable: bool,
            interested_clients: List[str] = None,
    ):
        super().__init__(
            name, description, price, dimensions, serial_number,
            quantity, weight, manufacturing_country, interested_clients,
        )
        self.expandable = expandable
        self.how_many_seats = how_many_seats
        self.is_foldable = is_foldable


class Closet(Furniture):
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
            has_mirrors: bool,
            number_of_shelves: int,
            interested_clients: List[str] = None,
    ):
        super().__init__(
            name, description, price, dimensions, serial_number,
            quantity, weight, manufacturing_country, interested_clients,
        )
        self.has_mirrors = has_mirrors
        self.number_of_shelves = number_of_shelves
