from furniture import Chair, Sofa, Table, Bed, Closet


class FurnitureFactory:
    @staticmethod
    def create_furniture(furniture_desc):
        """
        Factory method to create furniture objects.

        Parameters:
        furniture_desc: Dictionary containing furniture attributes.

        Outputs:
        Instance of the specified furniture class.
        """
        if not (furniture_desc.get('serial_number') and furniture_desc.get('name') and furniture_desc.get('price')):
            raise ValueError("Basic attributes missing, failed to create furniture object")

        furniture_classes = {
            "Chair": Chair,
            "Sofa": Sofa,
            "Table": Table,
            "Bed": Bed,
            "Closet": Closet
        }
        furniture_type = furniture_desc.pop('type')

        if not furniture_type in furniture_classes:
            raise ValueError(f"Unknown furniture type: {furniture_type}")

        if furniture_type == 'Chair':
            return Chair(**furniture_desc)
        elif furniture_type == 'Sofa':
            return Sofa(**furniture_desc)
        elif furniture_type == 'Table':
            return Table(**furniture_desc)
        elif furniture_type == 'Bed':
            return Bed(**furniture_desc)
        elif furniture_type == 'Closet':
            return Closet(**furniture_desc)
        else:
            raise ValueError(f"Unknown furniture type: {furniture_type}")
