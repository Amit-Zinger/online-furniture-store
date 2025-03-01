import pytest
from models.factory import FurnitureFactory
from models.furniture import Chair, Sofa, Table, Bed, Closet


@pytest.fixture
def valid_chair_desc():
    """Fixture providing a valid chair description dictionary."""
    return {
        "type": "Chair",
        "name": "Office Chair",
        "description": "Comfortable office chair",
        "price": 150.0,
        "dimensions": "50x50x100 cm",
        "serial_number": "CH001",
        "quantity": 10,
        "weight": 15.0,
        "manufacturing_country": "Germany",
        "has_wheels": True,
        "how_many_legs": 5,
    }


def test_create_valid_furniture(valid_chair_desc):
    """Test valid furniture creation."""
    chair = FurnitureFactory.create_furniture(valid_chair_desc)
    assert isinstance(chair, Chair)


def test_missing_furniture_type(valid_chair_desc):
    """Test that missing 'type' raises an error."""
    invalid_desc = valid_chair_desc.copy()
    del invalid_desc["type"]

    with pytest.raises(ValueError, match="Furniture type is required"):
        FurnitureFactory.create_furniture(invalid_desc)


def test_unknown_furniture_type(valid_chair_desc):
    """Test that an unknown furniture type raises an error."""
    invalid_desc = valid_chair_desc.copy()
    invalid_desc["type"] = "UnknownType"

    with pytest.raises(ValueError, match="Unknown furniture type"):
        FurnitureFactory.create_furniture(invalid_desc)


def test_missing_required_attributes(valid_chair_desc):
    """Test that missing required attributes raise an error."""
    invalid_desc = valid_chair_desc.copy()
    del invalid_desc["price"]

    with pytest.raises(ValueError, match="Missing required attributes"):
        FurnitureFactory.create_furniture(invalid_desc)


def test_register_new_furniture_type():
    """Test registering a new furniture type dynamically with full attributes."""

    class CustomFurniture:
        def __init__(self, **kwargs):
            self.name = kwargs.get("name", "Custom")
            self.description = kwargs.get("description", "Custom furniture")
            self.price = kwargs.get("price", 100.0)
            self.dimensions = kwargs.get("dimensions", "50x50x50 cm")
            self.serial_number = kwargs.get("serial_number", "CF001")
            self.quantity = kwargs.get("quantity", 5)
            self.weight = kwargs.get("weight", 20.0)
            self.manufacturing_country = kwargs.get("manufacturing_country", "USA")
            self.custom_feature = kwargs.get("custom_feature", "Special")

    FurnitureFactory.register_furniture("CustomFurniture", CustomFurniture)

    custom_desc = {
        "type": "CustomFurniture",
        "name": "Custom Chair",
        "description": "Handmade wooden chair",
        "price": 250.0,
        "dimensions": "60x60x80 cm",
        "serial_number": "CC001",
        "quantity": 10,
        "weight": 15.0,
        "manufacturing_country": "Germany",
        "custom_feature": "Unique Design",
    }

    custom_obj = FurnitureFactory.create_furniture(custom_desc)

    assert isinstance(custom_obj, CustomFurniture)
    assert custom_obj.custom_feature == "Unique Design"



def test_register_invalid_furniture_type():
    """Test that registering an invalid furniture type raises an error."""
    with pytest.raises(ValueError, match="Furniture type name must be a non-empty string"):
        FurnitureFactory.register_furniture("", Chair)

    with pytest.raises(ValueError, match="The provided class must be callable"):
        FurnitureFactory.register_furniture("InvalidType", "NotAClass")


def test_create_furniture_with_negative_price(valid_chair_desc):
    """Test that creating furniture with a negative price raises an error."""
    invalid_desc = valid_chair_desc.copy()
    invalid_desc["price"] = -50.0

    with pytest.raises(ValueError, match="Price must be a positive value"):
        FurnitureFactory.create_furniture(invalid_desc)


def test_create_furniture_with_zero_quantity(valid_chair_desc):
    """Test that creating furniture with zero quantity raises an error."""
    invalid_desc = valid_chair_desc.copy()
    invalid_desc["quantity"] = 0

    with pytest.raises(ValueError, match="Quantity must be a positive value"):
        FurnitureFactory.create_furniture(invalid_desc)


def test_create_furniture_with_negative_weight(valid_chair_desc):
    """Test that creating furniture with a negative weight raises an error."""
    invalid_desc = valid_chair_desc.copy()
    invalid_desc["weight"] = -10.0

    with pytest.raises(ValueError, match="Weight must be a positive value"):
        FurnitureFactory.create_furniture(invalid_desc)


def test_create_furniture_invalid_arguments():
    """Tests that passing incorrect arguments raises TypeError."""
    invalid_desc = {
        "type": "Chair",
        "name": "Broken Chair",
        "description": "Invalid object test",
        "price": "Not a number",  # Invalid price type
        "dimensions": "50x50x100 cm",
        "serial_number": "CH002",
        "quantity": "Ten",  # Invalid quantity type
        "weight": -5.0,  # Invalid negative weight
        "manufacturing_country": "USA",
        "has_wheels": True,
        "how_many_legs": 5,
    }
    with pytest.raises(TypeError, match="Failed to create furniture"):
        FurnitureFactory.create_furniture(invalid_desc)

