from models import Product
from typing import List

class ShoppingListHandler:
    # ------------------------| CONSTRUCTOR |------------------------
    def __init__(self) -> None:
        self.products_list: List[Product] = []

    # ------------------------| ADD |------------------------
    def add_product(self, name: str, quantity: int) -> None:
        self.products_list.append(Product(name.strip(), quantity))

    # ------------------------| REMOVE |------------------------
    def remove_product(self, name: str) -> None:
        self.products_list = [product for product in self.products_list if (product.name).lower() != name.lower()]

    # ------------------------| EDIT |------------------------
    def edit_product(self, name: str, new_name: str, new_quantity: int) -> None:
        for product in self.products_list:
            if (product.name).lower() == name.lower():
                product.name = new_name if len(new_name) > 0 else name
                product.quantity = new_quantity
                return 

    # ------------------------| MARK |------------------------
    def mark_as_purchased(self, name: str) -> None:
        for product in self.products_list:
            if (product.name).lower() == name.lower():
                product.purchased =  not product.purchased
                return