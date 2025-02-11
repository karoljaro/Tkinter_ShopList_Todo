from domain.entities.product import Product
from domain.interfaces.product_repository import ProductRepository
from typing import List, Optional

class InMemoryProductRepository(ProductRepository):
    def __init__(self) -> None:
        self.products: List[Product] = []

    def add_product(self, product) -> None:
        self.products.append(product)
    
    def remove_product(self, product_id) -> None:
        self.product = [product for product in self.products if product.id != product_id]

    def update_product(self, product) -> None:
        for idx, existing_product in enumerate(self.products):
            if existing_product.id == product.id:
                self.product[idx] = product
                break

    def get_all_products(self) -> List[Product]:
        return self.products
    
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        for product in self.products:
            if product.id == product_id:
                return product 
        return None
    