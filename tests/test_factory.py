import pytest
from models.factory import FurnitureFactory


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
def test_furniture_creation(furniture_type, attributes):
    """Test that different furniture types can be created with the correct attributes."""
    furniture_data = {
        "name": f"{furniture_type} Model X",
        "description": "A sample description",
        "price": 300.0,
        "dimensions": "120x120x120 cm",
        "serial_number": "UF001",
        "quantity": 2,
        "weight": 40.0,
        "manufacturing_country": "France",
        "type": furniture_type,
        **attributes,
    }
    furniture = FurnitureFactory.create_furniture(furniture_data)
    for key, value in attributes.items():
        assert getattr(furniture, key) == value


@pytest.mark.parametrize(
    "furniture_type, missing_attribute",
    [
        ("Sofa", "how_many_seats"),
        ("Table", "expandable"),
        ("Closet", "number_of_shelves"),
        ("Chair", "how_many_legs"),
        ("Bed", "has_storage"),
    ],
)
def test_missing_furniture_specific_attributes(furniture_type, missing_attribute):
    """Test that missing a required attribute raises a ValueError."""
    valid_data = {
        "name": f"{furniture_type} Model X",
        "description": "A sample description",
        "price": 300.0,
        "dimensions": "120x120x120 cm",
        "serial_number": "UF002",
        "quantity": 2,
        "weight": 40.0,
        "manufacturing_country": "Germany",
        "type": furniture_type,
        "has_wheels": True,
        "how_many_legs": 4,
        "how_many_seats": 2,
        "expandable": False,
        "can_turn_to_bed": False,
        "has_storage": False,
        "has_back": False,
        "has_mirrors": False,
        "number_of_shelves": 3,
        "how_many_doors": 2,
    }

    del valid_data[missing_attribute]  # מוחקים את המאפיין החיוני

    with pytest.raises(ValueError, match=f"{furniture_type} requires additional attributes"):
        FurnitureFactory.create_furniture(valid_data)  # ניסיון ליצור את הרהיט ללא המאפיין החיוני


def test_create_furniture_unknown_type():
    """Test creating furniture with an unknown type."""
    furniture_data = {
        "name": "Unknown Model",
        "description": "A sample description",
        "price": 300.0,
        "dimensions": "120x120x120 cm",
        "serial_number": "UF003",
        "quantity": 2,
        "weight": 40.0,
        "manufacturing_country": "France",
        "type": "UnknownType",
    }
    with pytest.raises(ValueError, match="Unknown furniture type"):
        FurnitureFactory.create_furniture(furniture_data)


def test_create_furniture_invalid_parameters():
    """Test handling of TypeError when creating furniture with invalid parameters."""
    furniture_data = {
        "name": "Faulty Chair",
        "description": "A bad chair",
        "price": 150.0,
        "dimensions": "90x90x90 cm",
        "serial_number": "CH002",
        "quantity": 3,
        "weight": 25.0,
        "manufacturing_country": "Italy",
        "type": "Chair",
        "has_wheels": "invalid_boolean",
        "how_many_legs": 4,
    }
    with pytest.raises(TypeError, match="Invalid type for has_wheels, expected bool"):
        FurnitureFactory.create_furniture(furniture_data)

