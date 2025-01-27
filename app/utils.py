def calc_discount(price: float, discount_percentage: float) -> float:
    """
    Calculate the discounted price for a furniture item.

    Parameters:
    price (float): The original price of the item.
    discount_percentage (float): The percentage discount to apply.

    Returns:
    float: The discounted price.
    """
    if discount_percentage < 0 or discount_percentage > 100:
        raise ValueError("Discount percentage must be between 0 and 100.")

    discounted_price = price * (1 - discount_percentage / 100)
    return round(discounted_price, 2)
