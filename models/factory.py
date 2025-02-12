from models.furniture import Chair, Sofa, Table, Bed, Closet

furniture_classes = {
    "Chair": Chair,
    "Sofa": Sofa,
    "Table": Table,
    "Bed": Bed,
    "Closet": Closet
}


class FurnitureFactory:
    """
    Factory class for creating furniture objects dynamically.
    """

    @staticmethod
    def register_furniture(name, cls):
        """
        Allows dynamic registration of new furniture types.

        :param name: The name of the new furniture type.
        :param cls: The class representing the new furniture type.
        """
        furniture_classes[name] = cls

    @staticmethod
    def create_furniture(furniture_desc):
        """
        Factory method to create furniture objects.

        :param furniture_desc: Dictionary containing furniture attributes.
        :return: An instance of the specified furniture class.
        :raises ValueError: If furniture type is missing or unknown.
        """
        furniture_type = furniture_desc.get('type')
        if furniture_type not in furniture_classes:
            raise ValueError(f"Unknown furniture type: {furniture_type}")

        furniture_desc.pop('type')  # Remove 'type' after validation

        # Add custom handling for specific attributes
        if furniture_type == 'Sofa':
            if 'how_many_seats' not in furniture_desc:
                raise ValueError("Sofa requires 'how_many_seats'")
            if 'can_turn_to_bed' not in furniture_desc:
                raise ValueError("Sofa requires 'can_turn_to_bed'")

        if furniture_type == 'Table':
            if 'is_foldable' not in furniture_desc:
                raise ValueError("Table requires 'is_foldable'")

        try:
            return furniture_classes[furniture_type](**furniture_desc)
        except TypeError as e:
            raise TypeError(f"Failed to create furniture: {e}")
