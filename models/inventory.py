import pandas as pd
import os
from models.factory import FurnitureFactory


class Inventory:
    """
    Class Inventory to manage available furniture items.

    Features:
    - Add, remove, and update the quantity of furniture items.
    - Search for furniture items by attributes such as name, category, and price range.
    """

    def __init__(self, file_path):
        """
        Initialize the Inventory class with the given file path.

        Parameters:
        file_path: Path to the pickle file containing inventory data.
        """
        self.file_path = file_path
        try:
            # Check if file exists , if not create new one
            if not os.path.exists(file_path):
                data = {
                    "Chair": [[]],
                    "Sofa": [[]],
                    "Table": [[]],
                    "Bed": [[]],
                    "Closet": [[]],
                }
                self.data = pd.DataFrame(data)
                self.update_data()
                return
            self._load_data()
        except Exception as e:
            raise Exception(
                f"Failed to create Inventory object.\nChenk path to data file."
            )

    def _load_data(self):
        """
        Load inventory data from a pickle file.

        return:
        True if data uploaded and False if not.
        """
        try:
            self.data = pd.read_pickle(self.file_path)
            return True
        except BaseException:
            print("Failed to upload data to pickle file, check file path")
            return False

    def update_data(self):
        """
        Save the current inventory data to a pickle file.

        return:
        True if data updated and False if not.
        """
        try:
            self.data.to_pickle(self.file_path)
            return True
        except BaseException:
            print("Failed to update data to pickle file, check file path")
            return False

    def add_item(self, furniture_desc):
        """
        Add a new furniture item to the inventory.

        param:
        furniture_desc: Dictionary containing furniture attributes.

        return:
        True if item added and False if not.
        """
        # Creates furniture attribute
        if "type" in furniture_desc.keys():
            furniture_type = furniture_desc["type"]
            furniture_instance = FurnitureFactory.create_furniture(furniture_desc)
            if furniture_instance and self.data is not None:
                self.data.at[0, furniture_type].append(furniture_instance)
            else:
                print("Failed to create Furniture object.")
                return False
        else:
            print("Basic attributes missing fail to create furniture object.")
            return False
        return True

    def remove_item(self, furniture_atr=None, furniture_desc=None):
        """
        Remove a furniture item from the inventory.

        Parameters:
        furniture_item: Furniture object to be removed.
        furniture_desc: Dictionary containing furniture attributes.

        return:
        True if item removed and False if not.
        """
        if furniture_desc and furniture_atr is None:
            if "type" in furniture_desc.keys():
                furniture_atr = FurnitureFactory.create_furniture(furniture_desc)
            else:
                print("Basic attributes missing fail to create furniture object.")
                return False
        if furniture_atr:
            class_name = type(furniture_atr).__name__
            pd_spec_class = self.data[class_name][0]
            try:
                pd_spec_class.remove(furniture_atr)
            except ValueError:
                return False
            self.data.loc[0, class_name] = pd_spec_class
            return True

        print("No furniture object or furniture data delivered.")
        return False

    def update_quantity(self, furniture_atr, new_q):
        """
        Update the quantity of an existing furniture item.

        Parameters:
        furniture_item: Furniture object whose quantity needs to be updated.
        new_quantity: New quantity value.

        return:
        True if quantity updated and False if not.
        """
        # Find the furniture_atr in the data frame
        if furniture_atr:
            class_name = type(furniture_atr).__name__
            pd_spec_class = self.data[class_name][0]
            item_id = furniture_atr.serial_number
            flag = False
            for obj in pd_spec_class:
                if obj.serial_number == item_id:
                    obj.quantity = new_q
                    flag = True
                    break
            if not flag:
                return False
            self.data.loc[0, class_name] = pd_spec_class
            return True

    def search_by(self, name=None, category=None, price_range=None, **filters):
        """
        Search for furniture items based on attributes.

        Parameters:
        name: Name of the furniture item.
        category: Category of the furniture item.
        price_range: Tuple specifying min and max price range.
        filters: Additional attribute filters as key-value pairs.

        Outputs:
        List of furniture items that match the search criteria.
        """

        # Additional option to check according to other attributes of furniture
        # obj- Disabled
        def matches_filters(item):
            """
            Check if an item matches all provided filters.
            Parameters:
            item: Furniture object.
            Outputs:
            True if the item matches all filters, otherwise False.
            """
            for attr, value in filters.items():
                if not hasattr(item, attr) or getattr(item, attr) != value:
                    return False
            return True

        def match_price_range(item):
            """
            Check if the item's price is within the specified range.

            Parameters:
            item: Furniture object.

            Outputs:
            True if the price is within range, otherwise False.
            """
            if not hasattr(item, "price"):
                return False
            min_price, max_price = price_range
            return min_price <= item.price <= max_price

        def match_name(item):
            """
            Check if the item's name match the name given.

            Parameters:
            item: Furniture object.

            Outputs:
            True if the name match, otherwise False.
            """
            if not hasattr(item, "name") or getattr(item, "name") != name:
                return False
            return True

        furniture_classes = ["Chair", "Sofa", "Table", "Bed", "Closet"]
        result = None
        # Handling specific category of furniture
        if category:
            result = pd.DataFrame()
            result = pd.DataFrame({"object": self.data[category][0]})
        # Handling specific name of furniture
        if name:
            if result is None:
                result = pd.DataFrame()
                for fc in furniture_classes:
                    temp_df = pd.DataFrame({"object": self.data[fc][0]})
                    filtered_data = temp_df["object"].apply(match_name)
                    temp_df = temp_df[filtered_data]
                    result = pd.concat([result, temp_df], ignore_index=True)
            else:
                filtered_data = result["object"].apply(match_name)
                result = result[filtered_data]
        # Handling price range of furniture
        if price_range:
            if result is None:
                result = pd.DataFrame()
                for fc in furniture_classes:
                    temp_df = pd.DataFrame({"object": self.data[fc][0]})
                    filtered_data = temp_df["object"].apply(match_price_range)
                    temp_df = temp_df[filtered_data]
                    result = pd.concat([result, temp_df], ignore_index=True)
            else:
                filtered_data = result["object"].apply(match_price_range)
                result = result[filtered_data]

        # Apply additional filters - Disabled
        # if (filters):
        #     filtered_data = result.apply(match_price_range)
        #     result = result[filtered_data]

        if result is None or result.empty:
            return []

        return result["object"].tolist()


def create_inventory_with_furniture(file_path):
    """
    Create an Inventory instance and populate it with five different objects from each furniture type.

    Parameters:
    file_path: Path to the pickle file where inventory data is stored.
    """
    inventory = Inventory(file_path)

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
                furniture_desc.update({"has_wheels": i % 2 == 0, "how_many_legs": 4})
            elif furniture_type == "Sofa":
                furniture_desc.update(
                    {"can_turn_to_bed": i % 2 == 0, "how_many_seats": 3 + i}
                )
            elif furniture_type == "Table":
                furniture_desc.update(
                    {
                        "expandable": i % 2 == 0,
                        "how_many_seats": 4 + i,
                        "is_foldable": False,
                    }
                )
            elif furniture_type == "Bed":
                furniture_desc.update({"has_storage": i % 2 == 0, "has_back": True})
            elif furniture_type == "Closet":
                furniture_desc.update(
                    {"has_drawers": i % 2 == 0, "how_many_doors": 2 + i}
                )

            inventory.add_item(furniture_desc)

    inventory.update_data()
    print("Inventory populated with furniture items successfully.")
