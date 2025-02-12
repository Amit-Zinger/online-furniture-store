import pytest
from models.inventory import Inventory
import os


@pytest.fixture
def setup_inventory():
    """Fixture to create a fresh inventory with predefined furniture items."""
    test_file = "test_inventory.pkl"

    # Ensure a fresh test file is created
    if os.path.exists(test_file):
        os.remove(test_file)

    def create_inventory_with_furniture(file_path):
        """
        Create an Inventory instance and populate it with five different objects from each furniture type.

        Parameters:
        file_path: Path to the pickle file where inventory data is stored.
        """
        inventory_testing = Inventory(file_path)

        furniture_types = ["Chair", "Sofa", "Table", "Bed", "Closet"]

        for furniture_type in furniture_types:
            for i in range(5):
                furniture_desc = {
                    "type": furniture_type,
                    "name": f"{furniture_type} Model {i + 1}",
                    "description": f"A stylish {furniture_type} for home or office.",
                    "price": 100 + i * 50,
                    "dimensions": "100x50x75 cm",
                    "serial_number": f"SN{furniture_type}{i + 1}",
                    "quantity": 10 + i,
                    "weight": 20 + i * 5,
                    "manufacturing_country": "USA",
                }

                # Add specific attributes for each furniture type
                if furniture_type == "Chair":
                    furniture_desc.update(
                        {"has_wheels": i % 2 == 0, "how_many_legs": 4}
                    )
                elif furniture_type == "Sofa":
                    furniture_desc.update(
                        {"can_turn_to_bed": i % 2 == 0, "how_many_seats": 3 + i}
                    )
                elif furniture_type == "Table":
                    furniture_desc.update(
                        {"expandable": i % 2 == 0, "how_many_seats": 4 + i}
                    )
                elif furniture_type == "Bed":
                    furniture_desc.update({"has_storage": i % 2 == 0, "has_back": True})
                elif furniture_type == "Closet":
                    furniture_desc.update(
                        {
                            "how_many_doors": 2 + i,
                            "has_mirrors": True,
                            "number_of_shelves": i,
                        }
                    )

                inventory_testing.add_item(furniture_desc)

        inventory_testing.update_data()
        print("Inventory populated with furniture items successfully.")

    create_inventory_with_furniture(test_file)  # Populate inventory
    inventory = Inventory(test_file)

    return inventory, test_file


def test_add_item(setup_inventory):
    inventory, _ = setup_inventory
    initial_count = len(inventory.data["Chair"][0])

    furniture_desc = {
        "type": "Chair",
        "name": "Luxury Chair",
        "description": "Premium comfortable chair",
        "price": 250,
        "dimensions": "120x60x100 cm",
        "serial_number": "CH010",
        "quantity": 5,
        "weight": 20,
        "manufacturing_country": "Germany",
        "has_wheels": False,
        "how_many_legs": 4,
    }

    assert inventory.add_item(furniture_desc) is True
    assert len(inventory.data["Chair"][0]) == initial_count + 1


def test_remove_item(setup_inventory):
    inventory, _ = setup_inventory
    chair_obj = inventory.data["Chair"][0][0]

    assert inventory.remove_item(chair_obj) is True
    assert chair_obj not in inventory.data["Chair"][0]


def test_update_quantity(setup_inventory):
    inventory, _ = setup_inventory
    chair_obj = inventory.data["Chair"][0][0]

    assert inventory.update_quantity(chair_obj, 99) is True
    assert chair_obj.quantity == 99


def test_search_by_name(setup_inventory):
    inventory, _ = setup_inventory
    first_chair_name = inventory.data["Chair"][0][0].name

    results = inventory.search_by(name=first_chair_name)

    assert len(results) > 0
    assert all(obj.name == first_chair_name for obj in results)


def test_search_by_category(setup_inventory):
    inventory, _ = setup_inventory
    results = inventory.search_by(category="Sofa")

    assert len(results) == 5  # Expecting 5 sofas in the inventory
    assert all(type(obj).__name__ == "Sofa" for obj in results)


def test_search_by_price_range(setup_inventory):
    inventory, _ = setup_inventory
    results = inventory.search_by(price_range=(150, 300))

    # Since each furniture type has 5 items with increasing prices (100, 150, 200, 250, 300)
    expected_count = 5 * 4  # 3 price points per category across 5 categories
    assert len(results) == expected_count
    assert all(100 <= obj.price <= 300 for obj in results)


def test_search_by_name_and_price(setup_inventory):
    inventory, _ = setup_inventory
    chair_name = inventory.data["Chair"][0][1].name  # Selecting second chair

    results = inventory.search_by(name=chair_name, price_range=(100, 200))

    assert len(results) > 0
    assert all(obj.name == chair_name and 100 <= obj.price <= 200 for obj in results)


def test_search_by_category_and_price(setup_inventory):
    inventory, _ = setup_inventory
    results = inventory.search_by(category="Table", price_range=(100, 250))

    # Should find tables with prices 100, 150, 200, and 250
    expected_count = 4  # Since one price (300) is out of range
    assert len(results) == expected_count
    assert all(
        type(obj).__name__ == "Table" and 100 <= obj.price <= 250 for obj in results
    )


def test_search_by_name_category_and_price(setup_inventory):
    inventory, _ = setup_inventory
    sofa_name = inventory.data["Sofa"][0][2].name  # Selecting third sofa

    results = inventory.search_by(
        name=sofa_name, category="Sofa", price_range=(100, 300)
    )

    assert len(results) == 1  # Expecting only one exact match
    assert all(
        obj.name == sofa_name
        and type(obj).__name__ == "Sofa"
        and 100 <= obj.price <= 300
        for obj in results
    )


def test_update_data(setup_inventory):
    inventory, test_file = setup_inventory

    assert inventory.update_data() is True
    assert os.path.exists(test_file)

    # Reload inventory and verify that data persists
    new_inventory = Inventory(test_file)
    assert len(new_inventory.data["Chair"][0]) == 5  # Should still contain 5 chairs
