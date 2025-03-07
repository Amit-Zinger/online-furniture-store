import sys
import os
import pandas as pd
from typing import Optional, Dict, List, Tuple, Union
from models.factory import FurnitureFactory
from models.furniture import Furniture

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Define directory for inventory database

INVEN_FILE: str = os.path.join(
    os.path.join(os.path.dirname(__file__), ".."), "data/inventory.pkl"
)


class Inventory:
    """
    Class Inventory to manage available furniture items.

    Features:
    - Add, remove, and update the quantity of furniture items.
    - Search for furniture items by attributes such as name, category, and price range.
    """

    def __init__(self, file_path: str = INVEN_FILE) -> None:
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

    def _load_data(self) -> bool:
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

    def update_data(self) -> bool:
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

    def add_item(self, furniture_desc: Dict[str, Union[str, int, float]]) -> bool:
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

    def remove_item(
        self,
        furniture_atr: Optional[Furniture] = None,
        furniture_desc: Optional[Dict[str, Union[str, int, float]]] = None,
    ) -> bool:
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
        if furniture_atr and isinstance(furniture_atr, Furniture):
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

    def update_quantity(self, furniture_atr: Furniture, new_q: int) -> bool:
        """
        Update the quantity of an existing furniture item.

        Parameters:
        furniture_item: Furniture object whose quantity needs to be updated.
        new_quantity: New quantity value.

        return:
        True if quantity updated and False if not.
        """
        # Find the furniture_atr in the data frame
        if furniture_atr and isinstance(furniture_atr, Furniture):
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

    def search_by(
        self,
        name: Optional[str] = None,
        category: Optional[str] = None,
        price_range: Optional[Tuple[float, float]] = None,
    ) -> List[Furniture]:
        """
        Search for furniture items based on attributes, if no
         attributes passed return list with all the furniture objects.

        Parameters:
        name: Name of the furniture item.
        category: Category of the furniture item.
        price_range: Tuple specifying min and max price range.

        Outputs:
        List of furniture items that match the search criteria.
        """

        def match_price_range(item: Furniture) -> bool:
            """Check if the item's price is within the specified range."""
            if not hasattr(item, "price"):
                return False
            min_price, max_price = price_range
            return min_price <= item.price <= max_price

        def match_name(item: Furniture) -> bool:
            """Check if the item's name matches the given name."""
            if not hasattr(item, "name") or getattr(item, "name") != name:
                return False
            return True

        furniture_classes = ["Chair", "Sofa", "Table", "Bed", "Closet"]
        result = None

        # Ensure `self.data` is properly initialized
        if not hasattr(self, "data") or self.data.empty:
            return []

        # Returning all furniture objects in list
        if not (price_range or name or category):
            result = pd.DataFrame()
            for fc in furniture_classes:
                category_data = self.data.get(fc, pd.DataFrame())
                if not category_data.empty:
                    temp_df = pd.DataFrame({"object": category_data.iloc[0]})
                    result = pd.concat([result, temp_df], ignore_index=True)

        # Handling specific category of furniture
        if category:
            category_data = self.data.get(category, pd.DataFrame())
            if not category_data.empty:
                result = pd.DataFrame({"object": category_data.iloc[0]})

        # Handling specific name of furniture
        if name:
            if result is None:
                result = pd.DataFrame()
                for fc in furniture_classes:
                    category_data = self.data.get(fc, pd.DataFrame())
                    if not category_data.empty:
                        temp_df = pd.DataFrame({"object": category_data.iloc[0]})
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
                    category_data = self.data.get(fc, pd.DataFrame())
                    if not category_data.empty:
                        temp_df = pd.DataFrame({"object": category_data.iloc[0]})
                        filtered_data = temp_df["object"].apply(match_price_range)
                        temp_df = temp_df[filtered_data]
                        result = pd.concat([result, temp_df], ignore_index=True)
            else:
                filtered_data = result["object"].apply(match_price_range)
                result = result[filtered_data]

        if result is None or result.empty:
            return []

        return result["object"].tolist()
