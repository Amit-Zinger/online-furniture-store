import pytest
from models.furniture import Chair, Sofa, Table, Bed, Closet, Furniture


@pytest.mark.parametrize("furniture_class, attributes", [
    (Chair, {"has_wheels": True, "how_many_legs": 5}),
    (Sofa, {"how_many_seats": 3, "can_turn_to_bed": True}),
    (Table, {"expandable": True, "how_many_seats": 6, "can_fold": False}),
    (Bed, {"has_storage": True, "has_back": True}),
    (Closet, {"has_mirrors": True, "number_of_shelves": 5, "how_many_doors": 3})
])
def test_furniture_creation(furniture_class, attributes):
    """Test creation of all furniture types using polymorphism."""
    base_attributes = {
        "name": "Test Furniture",
        "description": "Sample description",
        "price": 500.0,
        "dimensions": "100x100x100 cm",
        "serial_number": "TF001",
        "quantity": 10,
        "weight": 50.0,
        "manufacturing_country": "USA",
    }
    obj_attributes = {**base_attributes, **attributes}
    furniture = furniture_class(**obj_attributes)
    assert isinstance(furniture, Furniture)
    for attr, value in attributes.items():
        assert getattr(furniture, attr) == value


@pytest.mark.parametrize("discount", [10, 50, 90])
def test_apply_discount_valid(discount):
    """Test valid discount application for multiple furniture types."""
    furniture = Chair(
        name="Discount Chair",
        description="Sample description",
        price=200.0,
        dimensions="50x50x100 cm",
        serial_number="DC001",
        quantity=5,
        weight=15.0,
        manufacturing_country="Germany",
        has_wheels=True,
        how_many_legs=4,
    )
    expected_price = round(200.0 * (1 - discount / 100), 2)
    furniture.apply_discount(discount)
    assert furniture.price == expected_price


@pytest.mark.parametrize("tax_rate", [0.05, 0.1, 0.2])
def test_apply_tax_valid(tax_rate):
    """Test valid tax application for multiple furniture types."""
    furniture = Sofa(
        name="Taxed Sofa",
        description="Sample description",
        price=500.0,
        dimensions="200x90x100 cm",
        serial_number="TS001",
        quantity=5,
        weight=40.0,
        manufacturing_country="Italy",
        how_many_seats=3,
        can_turn_to_bed=True,
    )
    expected_price = round(500.0 * (1 + tax_rate), 2)
    furniture.apply_tax(tax_rate)
    assert furniture.price == expected_price


@pytest.mark.parametrize("deduction, expected", [(2, 8), (5, 5), (9, 1)])
def test_deduct_from_inventory_valid(deduction, expected):
    """Test deducting stock in multiple scenarios."""
    furniture = Table(
        name="Stock Table",
        description="Sample description",
        price=300.0,
        dimensions="180x90x75 cm",
        serial_number="ST001",
        quantity=10,
        weight=35.0,
        manufacturing_country="Sweden",
        expandable=True,
        how_many_seats=6,
        can_fold=False,
    )
    furniture.deduct_from_inventory(deduction)
    assert furniture.quantity == expected


@pytest.mark.parametrize("deduction", [11, 20])
def test_deduct_from_inventory_invalid(deduction):
    """Test deduction beyond available stock should raise error."""
    furniture = Bed(
        name="Limited Bed",
        description="Sample description",
        price=800.0,
        dimensions="200x180x60 cm",
        serial_number="LB001",
        quantity=10,
        weight=80.0,
        manufacturing_country="France",
        has_storage=True,
        has_back=True,
    )
    with pytest.raises(ValueError, match="Not enough stock"):
        furniture.deduct_from_inventory(deduction)
