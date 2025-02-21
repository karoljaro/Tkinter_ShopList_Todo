from src.application.repositories.IProductRepository import IProductRepository
from src.domain.Product_Entity import _Product
from typing import List, Optional

class InMemoryProductRepository(IProductRepository):
    def __init__(self) -> None:
        self.__products: List[_Product] = []

    def add_product(self, product: _Product) -> None:
        if self.get_product_by_id(product.id) is not None:
            raise ValueError(f"Product with id {product.id} already exists.")
        self.__products.append(product)

    def get_all_products(self) -> List[_Product]:
        return self.__products
    
    def remove_product(self, product_id: str) -> None:
        product = self.get_product_by_id(product_id)
        if product is None:
            raise ValueError(f"Product with id {product_id} does not exist.")
        self.__products = [product for product in self.__products if product.id != product_id]

    def get_product_by_id(self, product_id: str) -> Optional[_Product]:
        for product in self.__products:
            if product.id == product_id:
                return product
        return None

    def update_product(self, product: _Product) -> None:
        for i, p in enumerate(self.__products):
            if p.id == product.id:
                self.__products[i] = product
                return
        raise ValueError(f"Product with id {product.id} does not exist.")