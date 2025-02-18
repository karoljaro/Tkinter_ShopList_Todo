def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as err:
            print(f"Error: {err}")
            raise
    return wrapper