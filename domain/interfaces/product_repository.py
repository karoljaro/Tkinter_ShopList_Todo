from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.product import Product

class ProductRepository(ABC):

    @abstractmethod
    def add_product(self, product: Product) -> None:
        pass

    @abstractmethod
    def get_all_products(self) -> List[Product]:
        pass

    @abstractmethod
    def remove_product(self, product_id: int) -> None:
        pass

    @abstractmethod
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def update_product(self, product: Product) -> None:
        pass