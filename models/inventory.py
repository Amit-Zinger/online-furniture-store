import pandas as pd
import os
from furniture_class import Furniture
from furniture_factory_class import FurnitureFactory
from user_class import User


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
                self.data = pd.DataFrame()
                self.update_data()
                return
            self.data = self._load_data()
        except Exception as e:
            raise Exception(f"Failed to create Inventory object.\nChenk path to data file.")

    def _load_data(self):
        """
        Load inventory data from a pickle file.

        Outputs:
        Data loaded from the pickle file.

        raises:
        IOError: If the data cannot be loaded.
        """
        try:
             pd.read_pickle(self.file_path)
        except Exception as e:
             raise IOError(f"Failed to load inventory data: {e}")

    def update_data(self):
        """
        Save the current inventory data to a pickle file.
        """
        self.data.to_pickle(self.file_path)


    def add_item(self , furnirue_desc):
        """
        Add a new furniture item to the inventory.

        param:
        furniture_desc: Dictionary containing furniture attributes.
        """
        # Creates furniture attribute
        if ('type' in furnirue_desc.keys()):
            furniture_type = furnirue_desc['type']
            furniture_atr = FurnitureFactory.create_furniture(furniture_type,furnirue_desc)
            if (furniture_atr):
                pd_spec_class = self.data[furniture_type]
                pd_spec_class = pd.concat([pd_spec_class, furniture_atr], ignore_index=True)
                self.data[furniture_type] = pd_spec_class
            else :
                raise ValueError("Failed to create Furniture object.")
        else:
            raise ValueError("Basic attributes missing fail to create furniture object")



    def remove_item(self, furniture_atr):
        """
        Remove a furniture item from the inventory.

        Parameters:
        furniture_item: Furniture object to be removed.
        """
        if (furniture_atr):
            class_name = (type(furniture_atr).__name__)
            pd_spec_class = self.data[class_name]
            pd_spec_class = pd_spec_class[pd_spec_class != furniture_atr]
            self.data[class_name] = pd_spec_class


    def update_quantity(self, furniture_atr, new_q):
        """
        Update the quantity of an existing furniture item.

        Parameters:
        furniture_item: Furniture object whose quantity needs to be updated.
        new_quantity: New quantity value.

        raises:
        ValueError: If the item is not found.
        """
        # Find the furniture_atr in the data frame
        if (furniture_atr):
            class_name = (type(furniture_atr).__name__)
            pd_spec_class = self.data[class_name]
            item_id = furniture_atr.serial_number
            flag= False
            for obj in pd_spec_class:
                if obj.serial_number == item_id:
                    obj.quantity = new_q
                    flag = True
                    break
            if not flag:
                raise ValueError(f"Item with ID {item_id} not found.")
            self.data[class_name] = pd_spec_class


    def search_by(self,name=None,category=None,price_range=None,**filters):
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
        # Additional option to check according to other attributes of furniture obj- Disabled
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
            if not hasattr(item, 'price'):
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
            if not hasattr(item, 'name') or getattr(item,'name') != name:
                return False
            return True

        # Handling specific category of furniture
        if (category):
            result= self.data[category]
        # Handling specific name of furniture
        if (name):
            filtered_data = result.apply(match_name)
            result= result[filtered_data]
        # Handling price range of furniture
        if (price_range):
            filtered_data = result.apply(match_price_range)
            result = result[filtered_data]

        # Apply additional filters - Disabled
        # if (filters):
        #     filtered_data = result.apply(match_price_range)
        #     result = result[filtered_data]

        return result.tolist()
