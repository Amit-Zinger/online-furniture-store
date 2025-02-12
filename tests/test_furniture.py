import unittest
from models.furniture import Chair, Sofa, Table, Bed, Closet


class TestFurniture(unittest.TestCase):
    """Unit test class for testing Furniture and its derived classes."""

    def setUp(self):
        """Initialize different types of furniture before each test."""
        self.chair = Chair(
            name="Office Chair",
            description="Ergonomic chair with wheels",
            price=120.0,
            dimensions="60x60x120 cm",
            serial_number="CH001",
            quantity=10,
            weight=15.5,
            manufacturing_country="Germany",
            has_wheels=True,
            how_many_legs=5
        )

        self.sofa = Sofa(
            name="Luxury Sofa",
            description="Comfortable 3-seater sofa",
            price=450.0,
            dimensions="200x90x100 cm",
            serial_number="SF001",
            quantity=5,
            weight=40.0,
            manufacturing_country="Italy",
            how_many_seats=3,
            can_turn_to_bed=True
        )

        self.table = Table(
            name="Dining Table",
            description="Large wooden dining table",
            price=300.0,
            dimensions="180x90x75 cm",
            serial_number="TB001",
            quantity=7,
            weight=35.0,
            manufacturing_country="Sweden",
            expandable=True,
            how_many_seats=6,
            is_foldable=False
        )

        self.bed = Bed(
            name="King Bed",
            description="Spacious bed with storage",
            price=700.0,
            dimensions="200x180x60 cm",
            serial_number="BD001",
            quantity=3,
            weight=80.0,
            manufacturing_country="France",
            has_storage=True,
            has_back=True
        )

        self.closet = Closet(
            name="Modern Closet",
            description="Spacious closet with sliding doors",
            price=600.0,
            dimensions="250x60x200 cm",
            serial_number="CL001",
            quantity=4,
            weight=100.0,
            manufacturing_country="USA",
            has_mirrors=True,
            number_of_shelves=5
        )

    def test_apply_discount(self):
        """Test discount application on furniture items."""
        self.chair.apply_discount(10)  # 10% discount
        self.assertEqual(self.chair.price, 108.0)

    def test_apply_tax(self):
        """Test tax application (17% default)."""
        self.sofa.apply_tax()
        self.assertAlmostEqual(self.sofa.price, 526.5, places=1)

    def test_deduct_from_inventory(self):
        """Test reducing the inventory count."""
        self.table.deduct_from_inventory(2)
        self.assertEqual(self.table.quantity, 5)

    def test_deduct_inventory_insufficient_stock(self):
        """Test inventory deduction failure when stock is insufficient."""
        with self.assertRaises(ValueError):
            self.bed.deduct_from_inventory(10)

    def test_furniture_attributes(self):
        """Verify correct initialization of class attributes."""
        self.assertEqual(self.chair.how_many_legs, 5)
        self.assertTrue(self.sofa.can_turn_to_bed)
        self.assertTrue(self.table.expandable)
        self.assertTrue(self.bed.has_storage)
        self.assertEqual(self.closet.number_of_shelves, 5)

if __name__ == '__main__':
    unittest.main()
