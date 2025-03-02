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
            # ✅ Remove any attributes that are not part of the constructor
            allowed_keys = ["name", "description", "price", "dimensions", "serial_number",
                            "quantity", "weight", "manufacturing_country", "has_wheels",
                            "how_many_legs", "can_turn_to_bed", "how_many_seats",
                            "expandable", "is_foldable", "has_storage", "has_back",
                            "how_many_doors", "has_mirrors", "number_of_shelves"]

            filtered_dict = {k: v for k, v in furniture_dict.items() if k in allowed_keys}
            return FurnitureFactory.create_furniture({"type": furniture_type, **filtered_dict})
    return furniture_dict
