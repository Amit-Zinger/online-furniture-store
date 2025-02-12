import unittest
from models.factory import FurnitureFactory
from models.furniture import Chair, Sofa


class TestFurnitureFactory(unittest.TestCase):
    """Unit test class for testing the FurnitureFactory."""

    def setUp(self):
        """Setup furniture descriptions before each test."""
        self.chair_desc = {
            "type": "Chair",
            "name": "Gaming Chair",
            "description": "Ergonomic gaming chair",
            "price": 200.0,
            "dimensions": "70x70x130 cm",
            "serial_number": "CH002",
            "quantity": 10,
            "weight": 18.0,
            "manufacturing_country": "USA",
            "has_wheels": True,
            "how_many_legs": 5
        }

        self.sofa_desc = {
            "type": "Sofa",
            "name": "Leather Sofa",
            "description": "Premium leather 4-seater sofa",
            "price": 750.0,
            "dimensions": "220x100x90 cm",
            "serial_number": "SF002",
            "quantity": 3,
            "weight": 55.0,
            "manufacturing_country": "Spain",
            "how_many_seats": 4,
            "can_turn_to_bed": False
        }

    def test_create_furniture_chair(self):
        """Test the creation of a chair using the factory."""
        chair = FurnitureFactory.create_furniture(self.chair_desc)
        self.assertIsInstance(chair, Chair)
        self.assertEqual(chair.name, "Gaming Chair")
        self.assertTrue(chair.has_wheels)

    def test_create_furniture_sofa(self):
        """Test the creation of a sofa using the factory."""
        sofa = FurnitureFactory.create_furniture(self.sofa_desc)
        self.assertIsInstance(sofa, Sofa)
        self.assertEqual(sofa.how_many_seats, 4)

    def test_invalid_furniture_type(self):
        """Test error handling for unknown furniture type."""
        invalid_desc = {"type": "Lamp", "name": "Modern Lamp"}
        with self.assertRaises(ValueError):
            FurnitureFactory.create_furniture(invalid_desc)

    def test_missing_attributes(self):
        """Test error handling for missing required attributes."""
        invalid_sofa_desc = self.sofa_desc.copy()
        del invalid_sofa_desc["how_many_seats"]
        with self.assertRaises(ValueError):
            FurnitureFactory.create_furniture(invalid_sofa_desc)

    def test_register_new_furniture_type(self):
        """Test registering a new furniture type dynamically."""
        class CustomFurniture:
            def __init__(self, **kwargs):
                self.custom_attribute = kwargs.get("custom_attribute", "Default")

        FurnitureFactory.register_furniture("CustomFurniture", CustomFurniture)

        custom_desc = {"type": "CustomFurniture", "custom_attribute": "Special Feature"}
        custom_obj = FurnitureFactory.create_furniture(custom_desc)

        self.assertIsInstance(custom_obj, CustomFurniture)
        self.assertEqual(custom_obj.custom_attribute, "Special Feature")


if __name__ == '__main__':
    unittest.main()
