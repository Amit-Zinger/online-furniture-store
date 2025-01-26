from furniture_class import Furniture

class FurnitureFactory:
    @staticmethod
    def create_furniture(furniture_type, **kwargs):
        """
        Factory method to create furniture objects.

        Parameters:
        furniture_type: Type of furniture (e.g., 'Chair', 'Sofa').
        kwargs: Attributes required to create the furniture object.

        Outputs:
        Instance of the specified furniture class.
        """
        if not (kwargs.get('serial_number') and kwargs.get('name') and kwargs.get('price')):
            raise ValueError("Basic attributes missing fail to create furniture object")

        # Creating Chair object
        if furniture_type == 'Chair':
            return Chair(
                name=kwargs.get('name', 'Unnamed'),
                description=kwargs.get('description', ''),
                price=kwargs.get('price', 0),
                dimensions=kwargs.get('dimensions', 'Unknown'),
                serial_number=kwargs.get('serial_number', 'Unknown'),
                quantity = kwargs.get('quantity', 0),
                weight=kwargs.get('weight', 0),
                manufacturing_country=kwargs.get('manufacturing_country', 'Unknown'),
                #Specific attributes for chair
                has_weels=kwargs.get('has_weels', False),
                how_many_legs=kwargs.get('how_many_legs', 'Unknown')
            )
        # Creating Sofa object
        elif furniture_type == 'Sofa':
            return Sofa(
                name=kwargs.get('name', 'Unnamed'),
                description=kwargs.get('description', ''),
                price=kwargs.get('price', 0),
                dimensions=kwargs.get('dimensions', 'Unknown'),
                serial_number=kwargs.get('serial_number', 'Unknown'),
                quantity=kwargs.get('quantity', 0),
                weight=kwargs.get('weight', 0),
                manufacturing_country=kwargs.get('manufacturing_country', 'Unknown'),
                # Specific attributes for sofa
                can_turn_to_bad=kwargs.get('can_turn_to_bad', False),
                how_many_seats=kwargs.get('how_many_seats', 'Unknown')
            )
        # Creating Table object
        elif furniture_type == 'Table':
            return Table(
                name=kwargs.get('name', 'Unnamed'),
                description=kwargs.get('description', ''),
                price=kwargs.get('price', 0),
                dimensions=kwargs.get('dimensions', 'Unknown'),
                serial_number=kwargs.get('serial_number', 'Unknown'),
                quantity=kwargs.get('quantity', 0),
                weight=kwargs.get('weight', 0),
                manufacturing_country=kwargs.get('manufacturing_country', 'Unknown'),
                # Specific attributes for table
                expandable=kwargs.get('expandable', False),
                how_many_seats=kwargs.get('how_many_seats', 'Unknown')
            )
        # Creating Bed object
        elif furniture_type == 'Bed':
            return Bed(
                name=kwargs.get('name', 'Unnamed'),
                description=kwargs.get('description', ''),
                price=kwargs.get('price', 0),
                dimensions=kwargs.get('dimensions', 'Unknown'),
                serial_number=kwargs.get('serial_number', 'Unknown'),
                quantity=kwargs.get('quantity', 0),
                weight=kwargs.get('weight', 0),
                manufacturing_country=kwargs.get('manufacturing_country', 'Unknown'),
                # Specific attributes for bad
                has_storage=kwargs.get('has_storage', False),
                has_back=kwargs.get('has_back', False)
            )
        # Creating Closet object
        elif furniture_type == 'Closet':
            return Closet(
                name=kwargs.get('name', 'Unnamed'),
                description=kwargs.get('description', ''),
                price=kwargs.get('price', 0),
                dimensions=kwargs.get('dimensions', 'Unknown'),
                serial_number=kwargs.get('serial_number', 'Unknown'),
                quantity=kwargs.get('quantity', 0),
                weight=kwargs.get('weight', 0),
                manufacturing_country=kwargs.get('manufacturing_country', 'Unknown'),
                # Specific attributes for closet
                has_drawers=kwargs.get('has_drawers', False),
                how_many_doors=kwargs.get('how_many_doors', 'Unknown')
            )
        else:
            raise ValueError(f"Unknown furniture type: {furniture_type}")
