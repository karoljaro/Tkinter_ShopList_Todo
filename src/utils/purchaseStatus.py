def get_purchase_status(purchased: bool) -> str:
    """
    Get the purchase status as a string based on the boolean value.

    :param purchased: The purchase status as a boolean.
    :return: "Purchased" if True, otherwise "Not Purchased".
    """
    return "Purchased" if purchased else "Not Purchased"
