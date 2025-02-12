from abc import ABC
from typing import List, Callable
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
        self.name = name
        self.description = description
        self.price = price
        self.dimensions = dimensions
        self.serial_number = serial_number
        self.quantity = quantity
        self.weight = weight
        self.manufacturing_country = manufacturing_country
        self.interested_clients = interested_clients if interested_clients else []
        self._observers: List[Callable] = []

    def add_observer(self, observer: Callable):
        """
        Add an observer (e.g., Inventory) to be notified on changes.
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: Callable):
        """
        Remove an observer.
        """
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, message: str):
        """
        Notify all observers about a change in quantity.
        """
        for observer in self._observers:
            observer(self, message)

    def apply_discount(self, discount_percentage: float):
        """
        Apply a discount to the price of the furniture.

        Parameters:
        discount_percentage (float): The percentage discount to apply.
        """
        self.price = calc_discount(self.price, discount_percentage)

    def apply_tax(self):
        """
        Apply tax to the price of the furniture.

        Parameters:
        tax_rate (float): The tax rate to apply (default is 10%).
        """
        self.price += self.price * 0.17


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
            name,
            description,
            price,
            dimensions,
            serial_number,
            quantity,
            weight,
            manufacturing_country,
            interested_clients,
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
            name,
            description,
            price,
            dimensions,
            serial_number,
            quantity,
            weight,
            manufacturing_country,
            interested_clients,
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
            name,
            description,
            price,
            dimensions,
            serial_number,
            quantity,
            weight,
            manufacturing_country,
            interested_clients,
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
            interested_clients: List[str] = None,
    ):
        super().__init__(
            name,
            description,
            price,
            dimensions,
            serial_number,
            quantity,
            weight,
            manufacturing_country,
            interested_clients,
        )
        self.expandable = expandable
        self.how_many_seats = how_many_seats


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
            how_many_doors: int,
            has_drawers: bool,
            interested_clients: List[str] = None,
    ):
        super().__init__(
            name,
            description,
            price,
            dimensions,
            serial_number,
            quantity,
            weight,
            manufacturing_country,
            interested_clients,
        )
        self.how_many_doors = how_many_doors
        self.has_drawers = has_drawers
