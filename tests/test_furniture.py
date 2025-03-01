import pytest
from models.furniture import Chair, Sofa, Table, Bed, Closet


@pytest.fixture
def sample_chair():
    """Fixture providing a sample Chair object."""
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
    """Fixture providing a sample Sofa object."""
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
    """Fixture providing a sample Table object."""
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
    """Fixture providing a sample Bed object."""
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
    """Fixture providing a sample Closet object."""
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
# Tests for apply_discount()
# ----------------------------------------
def test_apply_discount_valid(sample_chair):
    """Tests that a valid discount is correctly applied to the price."""
    sample_chair.apply_discount(10)  # 10% discount
    assert sample_chair.price == 90.0  # Expected price after discount


def test_apply_discount_invalid_negative(sample_chair):
    """Tests that a negative discount raises an error."""
    with pytest.raises(ValueError, match="Discount percentage must be between 0 and 100"):
        sample_chair.apply_discount(-5)


def test_apply_discount_invalid_above_100(sample_chair):
    """Tests that a discount above 100% raises an error."""
    with pytest.raises(ValueError, match="Discount percentage must be between 0 and 100"):
        sample_chair.apply_discount(110)


# ----------------------------------------
# Tests for apply_tax()
# ----------------------------------------
def test_apply_tax_default_rate(sample_sofa):
    """Tests that tax is applied correctly (default 17%)."""
    sample_sofa.apply_tax()
    assert round(sample_sofa.get_final_price(), 2) == round(450.0 * 1.17, 2)


def test_apply_tax_custom_rate(sample_table):
    """Tests applying a custom tax rate."""
    sample_table.apply_tax(0.1)  # 10% tax
    assert round(sample_table.get_final_price(), 2) == round(200.0 * 1.1, 2)


def test_apply_tax_invalid_negative(sample_table):
    """Tests that a negative tax rate raises an error with correct message."""
    with pytest.raises(ValueError, match="Tax rate must be a positive value."):
        sample_table.apply_tax(-0.05)


# ----------------------------------------
# Tests for deduct_from_inventory()
# ----------------------------------------
def test_deduct_from_inventory_valid(sample_bed):
    """Tests that inventory quantity is correctly reduced."""
    sample_bed.deduct_from_inventory(2)
    assert sample_bed.quantity == 1  # Expected quantity after deduction


def test_deduct_from_inventory_invalid(sample_bed):
    """Tests that attempting to deduct more than available raises an error."""
    with pytest.raises(ValueError, match="Not enough stock"):
        sample_bed.deduct_from_inventory(10)


# ----------------------------------------
# Tests for Furniture Attributes
# ----------------------------------------
def test_furniture_attributes(sample_chair, sample_sofa, sample_table, sample_bed, sample_closet):
    """Verifies correct initialization of furniture attributes."""
    assert sample_chair.how_many_legs == 5
    assert sample_sofa.can_turn_to_bed is True
    assert sample_table.expandable is True
    assert sample_bed.has_storage is True
    assert sample_closet.number_of_shelves == 5


# ----------------------------------------
# Edge Case Tests
# ----------------------------------------
def test_furniture_invalid_price():
    """Tests that creating a furniture item with a negative price raises an error."""
    with pytest.raises(ValueError, match="Price must be a positive value"):
        Chair(
            name="Broken Chair",
            description="Invalid price test",
            price=-100.0,
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


def test_furniture_zero_weight():
    """Tests that creating furniture with zero weight raises an error."""
    with pytest.raises(ValueError, match="Weight must be a positive value"):
        Table(
            name="Weightless Table",
            description="A table with zero weight",
            price=150.0,
            dimensions="100x60x75 cm",
            serial_number="TB002",
            quantity=5,
            weight=0.0,
            manufacturing_country="USA",
            expandable=True,
            how_many_seats=4,
            is_foldable=False,
        )


def test_furniture_zero_quantity():
    """Tests that creating furniture with zero quantity raises an error."""
    with pytest.raises(ValueError, match="Quantity must be a positive value"):
        Bed(
            name="Empty Bed",
            description="A bed with no stock",
            price=500.0,
            dimensions="200x150x60 cm",
            serial_number="BD002",
            quantity=0,
            weight=70.0,
            manufacturing_country="France",
            has_storage=True,
            has_back=True,
        )


def test_furniture_str_output(sample_chair):
    """Tests that the __str__ method returns the correct formatted string."""
    expected_output = "Office Chair - Ergonomic chair with wheels | Price: $117.0 | Stock: 10"
    sample_chair.apply_tax()  # מחושב עם מס ברירת מחדל 17%
    assert str(sample_chair) == expected_output
