from models.furniture import Furniture
from models.factory import FurnitureFactory


def serialize_furniture(furniture_obj):
    """Converts a Furniture object to a dictionary for JSON storage."""
    if isinstance(furniture_obj, Furniture):
        furniture_dict = vars(furniture_obj)
        furniture_dict["type"] = type(furniture_obj).__name__  # Store type for deserialization
        return furniture_dict
    return furniture_obj


def deserialize_furniture(furniture_dict):
    """Converts a dictionary back into a Furniture object."""
    if isinstance(furniture_dict, dict) and "serial_number" in furniture_dict:
        furniture_type = furniture_dict.pop("type", None)
        if furniture_type:
            #  Remove any attributes that are not part of the constructor
            allowed_keys = ["name", "description", "price", "dimensions", "serial_number",
                            "quantity", "weight", "manufacturing_country", "has_wheels",
                            "how_many_legs", "can_turn_to_bed", "how_many_seats",
                            "expandable", "can_fold", "has_storage", "has_back",
                            "how_many_doors", "has_mirrors", "number_of_shelves"]

            filtered_dict = {k: v for k, v in furniture_dict.items() if k in allowed_keys}
            return FurnitureFactory.create_furniture({"type": furniture_type, **filtered_dict})
    return furniture_dict
