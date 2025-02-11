from application.services.shopping_list_service import ShoppingListServices
from domain.entities.product import Product

class ManageShoppingList:
    def __init__(self, service: ShoppingListServices):
        self.service = service

    def add_product(self, id: int, name: str, quantity: int) -> None:
        product = Product(id, name, quantity)
        self.service.add_product(product)

    def remove_product(self, product_id: int) -> None:
        self.service.remove_product(product_id)

    def mark_as_purchased(self, product_id: int) -> None:
        product = self.service.get_product_by_id(product_id)
        if product:
            product.purchased = True
            product.status = "kupione"
            self.service.update_product(product)

    def get_all_products(self):
        return self.service.get_all_products()