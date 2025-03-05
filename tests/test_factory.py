import pytest
from models.factory import FurnitureFactory
from models.furniture import Chair, Sofa, Table, Bed, Closet, Furniture


@pytest.mark.parametrize("furniture_type, attributes", [
    (Chair, {"has_wheels": True, "how_many_legs": 5}),
    (Sofa, {"how_many_seats": 3, "can_turn_to_bed": True}),
    (Table, {"expandable": True, "how_many_seats": 6, "can_fold": False}),
    (Bed, {"has_storage": True, "has_back": True}),
    (Closet, {"has_mirrors": True, "number_of_shelves": 5, "how_many_doors": 3})
])
def test_create_valid_furniture(furniture_type, attributes):
    """Test valid furniture creation using polymorphism."""
    common_attributes = {
        "name": "Sample Furniture",
        "description": "A sample description",
        "price": 250.0,
        "dimensions": "100x100x100 cm",
        "serial_number": "SF001",
        "quantity": 5,
        "weight": 30.0,
        "manufacturing_country": "Germany"
    }
    furniture_attributes = {**common_attributes, **attributes}
    furniture = furniture_type(**furniture_attributes)
    assert isinstance(furniture, Furniture)
    for attr, value in attributes.items():
        assert getattr(furniture, attr) == value


def test_register_invalid_furniture_type():
    """Test that registering an invalid furniture type raises an error."""
    with pytest.raises(ValueError, match="Furniture type name must be a non-empty string"):
        FurnitureFactory.register_furniture("", Chair)
    with pytest.raises(ValueError, match="The provided class must be callable"):
        FurnitureFactory.register_furniture("InvalidType", "not a class")


def test_create_furniture_invalid_values():
    """Test invalid values across different furniture types using parameterization."""
    common_invalid_values = [
        ("price", -10.0, "Price must be a positive value"),
        ("quantity", -5, "Quantity must be a positive value"),
        ("weight", -20.0, "Weight must be a positive value")
    ]
    for furniture_type in [Chair, Sofa, Table, Bed, Closet]:
        for attribute, invalid_value, expected_message in common_invalid_values:
            attributes = {"name": "Invalid Furniture", "description": "A sample description", "price": 250.0,
                          "dimensions": "100x100x100 cm", "serial_number": "SF001", "quantity": 5, "weight": 30.0,
                          "manufacturing_country": "Germany", attribute: invalid_value}
            with pytest.raises(ValueError, match=expected_message):
                furniture_type(**attributes)
