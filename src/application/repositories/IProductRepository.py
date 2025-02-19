from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.Product_Entity import _Product

class IProductRepository(ABC):
    @abstractmethod
    def add_product(self, product: _Product) -> None:
        pass

    @abstractmethod
    def get_all_products(self) -> List[_Product]:
        pass

    @abstractmethod
    def remove_product(self, product_id: str) -> None:
        pass

    @abstractmethod
    def get_product_by_id(self, product_id: str) -> Optional[_Product]:
        pass

    @abstractmethod
    def update_product(self, product: _Product) -> None:
        pass