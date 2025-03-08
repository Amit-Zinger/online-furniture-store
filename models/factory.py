import sys
import os
from models.furniture import Chair, Sofa, Table, Bed, Closet
from models.furniture import Furniture

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# all the created furniture
FURNITURE_CLASSES = {
    "Chair": Chair,
    "Sofa": Sofa,
    "Table": Table,
    "Bed": Bed,
    "Closet": Closet,
}


class FurnitureFactory:
    """
    Factory class for creating furniture objects dynamically.
    """

    @staticmethod
    def register_furniture(name: str, cls: type) -> None:
        """
        Allows dynamic registration of new furniture types.

        :param name: The name of the new furniture type.
        :param cls: The class representing the new furniture type.
        :raises ValueError: If the name is empty or the class is invalid.
        """
        if not name or not isinstance(name, str):
            raise ValueError("Furniture type name must be a non-empty string.")
        if not callable(cls):
            raise ValueError("The provided class must be callable.")
        FURNITURE_CLASSES[name] = cls

    @staticmethod
    def create_furniture(furniture_desc: dict[str, any]) -> Furniture:
        """
        Factory method to create furniture objects.

        :param furniture_desc: Dictionary containing furniture attributes.
        :return: An instance of the specified furniture class.
        :raises ValueError: If furniture type is missing or unknown.
        """

        # furniture type
        furniture_type = furniture_desc.get("type")
        if not furniture_type:
            raise ValueError("Furniture type is required.")

        if furniture_type not in FURNITURE_CLASSES:
            raise ValueError(f"Unknown furniture type: {furniture_type}")

        furniture_desc.pop("type")

        required_attributes = [
            "name", "description", "price", "dimensions",
            "serial_number", "quantity", "weight", "manufacturing_country"
        ]
        missing_attributes = [
            attr for attr in required_attributes if attr not in furniture_desc
        ]
        if missing_attributes:
            raise ValueError(f"Missing required attributes: {', '.join(missing_attributes)}")

        # Validate specific furniture attributes
        FurnitureFactory._validate_furniture_specifics(furniture_type, furniture_desc)

        # **New: Validate attribute types**
        type_validations = {
            "price": float,
            "quantity": int,
            "weight": float,
            "has_wheels": bool,
            "how_many_legs": int,
            "can_turn_to_bed": bool,
            "how_many_seats": int,
            "expandable": bool,
            "can_fold": bool,
            "has_storage": bool,
            "has_back": bool,
            "how_many_doors": int,
            "has_mirrors": bool,
            "number_of_shelves": int,
        }

        for attr, expected_type in type_validations.items():
            if attr in furniture_desc and not isinstance(furniture_desc[attr], expected_type):
                raise TypeError(f"Invalid type for {attr}. Expected {expected_type.__name__}.")

        # Try creating the furniture object
        try:
            return FURNITURE_CLASSES[furniture_type](**furniture_desc)
        except TypeError as e:
            raise TypeError(f"Failed to create furniture '{furniture_type}': {e}")

    @staticmethod
    def _validate_furniture_specifics(furniture_type, furniture_desc):
        """
        Ensures furniture-specific required attributes exist.

        :param furniture_type: The type of furniture.
        :param furniture_desc: The dictionary containing furniture attributes.
        :raises ValueError: If required attributes for a specific furniture type are missing.
        """
        required_specifics = {
            "Sofa": ["how_many_seats", "can_turn_to_bed"],
            "Table": ["expandable", "how_many_seats", "can_fold"],
            "Closet": ["has_mirrors", "number_of_shelves", "how_many_doors"],
            "Chair": ["has_wheels", "how_many_legs"],
            "Bed": ["has_storage", "has_back"],
        }

        missing_specifics = [
            attr
            for attr in required_specifics.get(furniture_type, [])
            if attr not in furniture_desc
        ]

        if missing_specifics:
            raise ValueError(
                f"{furniture_type} requires additional attributes: {', '.join(missing_specifics)}"
            )
