from domain.entities.product import Product
from domain.interfaces.product_repository import ProductRepository
from typing import List, Optional

class ShoppingListServices:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def add_product(self, product: Product) -> None:
        self.repository.add_product(product)

    def remove_product(self, product_id: int) -> None:
        self.repository.remove_product(product_id)

    def update_product(self, product: Product) -> None:
        self.repository.update_product(product)

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        return self.repository.get_product_by_id(product_id)
    
    def get_all_products(self) -> List[Product]:
        return self.repository.get_all_products()