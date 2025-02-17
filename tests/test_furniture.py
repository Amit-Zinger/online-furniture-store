import pytest
import sys
import os

# Add the project root directory to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from models.furniture import Chair, Sofa, Table, Bed, Closet


@pytest.fixture
def sample_chair():
    """Returns a sample Chair object for testing."""
    return Chair(
        name="Office Chair",
        description="Ergonomic chair with wheels",
        price=100.0,
        dimensions="60x60x120 cm",
        serial_number="CH001",
        quantity=10,
        weight=15.5,
        manufacturing_country="Germany",
        has_wheels=True,
        how_many_legs=5,
    )


@pytest.fixture
def sample_sofa():
    """Returns a sample Sofa object for testing."""
    return Sofa(
        name="Luxury Sofa",
        description="Comfortable 3-seater sofa",
        price=450.0,
        dimensions="200x90x100 cm",
        serial_number="SF001",
        quantity=5,
        weight=40.0,
        manufacturing_country="Italy",
        how_many_seats=3,
        can_turn_to_bed=True,
    )

@pytest.fixture
def sample_table():
    """Returns a sample Table object for testing."""
    return Table(
        name="Dining Table",
        description="Large wooden dining table",
        price=200.0,
        dimensions="180x90x75 cm",
        serial_number="TB001",
        quantity=7,
        weight=35.0,
        manufacturing_country="Sweden",
        expandable=True,
        how_many_seats=6,
        is_foldable=False,
    )

@pytest.fixture
def sample_bed():
    """Returns a sample Bed object for testing."""
    return Bed(
        name="King Bed",
        description="Spacious bed with storage",
        price=700.0,
        dimensions="200x180x60 cm",
        serial_number="BD001",
        quantity=3,
        weight=80.0,
        manufacturing_country="France",
        has_storage=True,
        has_back=True,
    )

@pytest.fixture
def sample_closet():
    """Returns a sample Closet object for testing."""
    return Closet(
        name="Modern Closet",
        description="Spacious closet with sliding doors",
        price=600.0,
        dimensions="250x60x200 cm",
        serial_number="CL001",
        quantity=4,
        weight=100.0,
        manufacturing_country="USA",
        has_mirrors=True,
        number_of_shelves=5,
        how_many_doors=3,
    )

# ----------------------------------------
# ✅ Tests for apply_discount()
# ----------------------------------------

def test_apply_discount_valid(sample_chair):
    """Tests that a valid discount is correctly applied to the price."""
    sample_chair.apply_discount(10)  # 10% discount
    assert sample_chair.price == 90.0  # Expected price after discount

def test_apply_discount_invalid_negative(sample_chair):
    """Tests that a negative discount raises an error."""
    with pytest.raises(ValueError):
        sample_chair.apply_discount(-5)  # Should raise ValueError

def test_apply_discount_invalid_above_100(sample_chair):
    """Tests that a discount above 100% raises an error."""
    with pytest.raises(ValueError):
        sample_chair.apply_discount(110)  # Should raise ValueError

# ----------------------------------------
# ✅ Tests for apply_tax()
# ----------------------------------------

def test_apply_tax_default_rate(sample_sofa):
    """Tests that tax is applied correctly (default 17%)."""
    sample_sofa.apply_tax()
    assert round(sample_sofa.price, 2) == 526.5  # Expected price after tax (450 * 1.17)

def test_apply_tax_custom_rate(sample_table):
    """Tests applying a custom tax rate."""
    sample_table.apply_tax(0.1)  # 10% tax
    assert round(sample_table.price, 2) == 220.0  # Expected price (200 * 1.10)

def test_apply_tax_invalid_negative(sample_table):
    """Tests that a negative tax rate raises an error."""
    with pytest.raises(ValueError):
        sample_table.apply_tax(-0.05)  # Should raise ValueError

# ----------------------------------------
# ✅ Tests for deduct_from_inventory()
# ----------------------------------------

def test_deduct_from_inventory_valid(sample_bed):
    """Tests that inventory quantity is correctly reduced."""
    sample_bed.deduct_from_inventory(2)
    assert sample_bed.quantity == 1  # Expected quantity after deduction

def test_deduct_from_inventory_invalid(sample_bed):
    """Tests that attempting to deduct more than available raises an error."""
    with pytest.raises(ValueError):
        sample_bed.deduct_from_inventory(10)  # Should raise ValueError

# ----------------------------------------
# ✅ Tests for Furniture Attributes
# ----------------------------------------

def test_furniture_attributes(sample_chair, sample_sofa, sample_table, sample_bed, sample_closet):
    """Verifies correct initialization of furniture attributes."""
    assert sample_chair.how_many_legs == 5
    assert sample_sofa.can_turn_to_bed is True
    assert sample_table.expandable is True
    assert sample_bed.has_storage is True
    assert sample_closet.number_of_shelves == 5

# ----------------------------------------
# ✅ Edge Case Tests
# ----------------------------------------

def test_furniture_invalid_price():
    """Tests that creating a furniture item with a negative price raises an error."""
    with pytest.raises(ValueError):
        Chair(
            name="Broken Chair",
            description="Invalid price test",
            price=-100.0,  # Negative price
            dimensions="50x50x100 cm",
            serial_number="CH002",
            quantity=5,
            weight=12,
            manufacturing_country="USA",
            has_wheels=True,
            how_many_legs=5,
        )

def test_furniture_out_of_stock(sample_bed):
    """Tests that if stock reaches 0, is_out_of_stock() returns True."""
    sample_bed.deduct_from_inventory(3)
    assert sample_bed.is_out_of_stock() is True
