import pytest
from models.factory import FurnitureFactory, FURNITURE_CLASSES
from models.furniture import Furniture


@pytest.mark.parametrize(
    "furniture_type, attributes",
    [
        ("Chair", {"has_wheels": True, "how_many_legs": 5}),
        ("Sofa", {"how_many_seats": 3, "can_turn_to_bed": True}),
        ("Table", {"expandable": True, "how_many_seats": 6, "can_fold": False}),
        ("Bed", {"has_storage": True, "has_back": True}),
        ("Closet", {"has_mirrors": True, "number_of_shelves": 5, "how_many_doors": 3}),
    ],
)
def test_create_furniture_using_factory(furniture_type, attributes):
    """Test creating furniture via the FurnitureFactory.create_furniture method."""
    common_attributes = {
        "name": "Sample Furniture",
        "description": "A sample description",
        "price": 250.0,
        "dimensions": "100x100x100 cm",
        "serial_number": "SF001",
        "quantity": 5,
        "weight": 30.0,
        "manufacturing_country": "Germany",
        "type": furniture_type,
    }
    furniture_attributes = {**common_attributes, **attributes}
    furniture = FurnitureFactory.create_furniture(furniture_attributes)
    assert isinstance(furniture, Furniture)
    for attr, value in attributes.items():
        assert getattr(furniture, attr) == value


def test_register_valid_furniture_type():
    """Test registering a valid new furniture type."""
    class CustomFurniture(Furniture):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

    FurnitureFactory.register_furniture("CustomFurniture", CustomFurniture)
    assert "CustomFurniture" in FURNITURE_CLASSES


def test_create_furniture_missing_type():
    """Test creating furniture without specifying type should raise an error."""
    with pytest.raises(ValueError, match="Furniture type is required."):
        FurnitureFactory.create_furniture({
            "name": "Test",
            "description": "Missing type",
            "price": 100,
            "dimensions": "50x50x50 cm",
            "serial_number": "M001",
            "quantity": 10,
            "weight": 5,
            "manufacturing_country": "USA"
        })


def test_create_furniture_unknown_type():
    """Test creating furniture with an unknown type should raise an error."""
    with pytest.raises(ValueError, match="Unknown furniture type: UnknownType"):
        FurnitureFactory.create_furniture({
            "type": "UnknownType",
            "name": "Test",
            "description": "Unknown type",
            "price": 100,
            "dimensions": "50x50x50 cm",
            "serial_number": "M001",
            "quantity": 10,
            "weight": 5,
            "manufacturing_country": "USA"
        })


def test_create_furniture_missing_required_attributes():
    """Test creating furniture with missing required attributes should raise an error."""
    with pytest.raises(ValueError, match="Missing required attributes: description, price"):
        FurnitureFactory.create_furniture({
            "type": "Chair",
            "name": "Test Chair",
            "dimensions": "50x50x50 cm",
            "serial_number": "M002",
            "quantity": 10,
            "weight": 5,
            "manufacturing_country": "USA"
        })


def test_create_furniture_missing_required_fields():
    """Test missing required fields when creating furniture."""
    with pytest.raises(ValueError, match="Missing required attributes"):
        FurnitureFactory.create_furniture({
            "type": "Chair",
            "name": "Sample Chair",
            "price": 250.0,
            "dimensions": "100x100x100 cm",
            "serial_number": "SF001",
            "quantity": 5,
            "weight": 30.0,
            "manufacturing_country": "Germany",
        })


def test_create_furniture_invalid_specific_attributes():
    """Test missing specific attributes required by _validate_furniture_specifics."""
    with pytest.raises(ValueError, match="Chair requires additional attributes"):
        FurnitureFactory.create_furniture({
            "type": "Chair",
            "name": "Sample Chair",
            "description": "A sample chair",
            "price": 250.0,
            "dimensions": "100x100x100 cm",
            "serial_number": "SF002",
            "quantity": 5,
            "weight": 30.0,
            "manufacturing_country": "Germany",
        })


def test_create_furniture_invalid_type():
    """Test creating furniture with an invalid attribute type should raise TypeError."""
    with pytest.raises(TypeError, match="Invalid type for has_wheels"):
        FurnitureFactory.create_furniture({
            "type": "Chair",
            "name": "Sample Chair",
            "description": "A sample chair",
            "price": 250.0,
            "dimensions": "100x100x100 cm",
            "serial_number": "SF003",
            "quantity": 5,
            "weight": 30.0,
            "manufacturing_country": "Germany",
            "has_wheels": "INVALID_TYPE",
            "how_many_legs": 4
        })
