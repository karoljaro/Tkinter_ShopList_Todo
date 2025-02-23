def handle_exceptions(func):
    """
    Decorator to handle exceptions for a function.

    :param func: The function to wrap with exception handling.
    :return: The wrapped function.
    """
    def wrapper(*args, **kwargs):
        """
        Wrapper function to catch and handle exceptions.

        :param args: Positional arguments for the wrapped function.
        :param kwargs: Keyword arguments for the wrapped function.
        :return: The result of the wrapped function, if no exception occurs.
        :raises ValueError: If a ValueError is raised by the wrapped function.
        """
        try:
            return func(*args, **kwargs)
        except ValueError as err:
            print(f"Error: {err}")
            raise
    return wrapper