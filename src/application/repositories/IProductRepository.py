from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.Product_Entity import _Product


class IProductRepository(ABC):
    """
    Interface for product repository.
    """

    @abstractmethod
    def add_product(self, product: _Product) -> None:
        """
        Add a new product to the repository.

        :param product: The product to add.
        """
        pass

    @abstractmethod
    def get_all_products(self) -> List[_Product]:
        """
        Retrieve all products from the repository.

        :return: A list of all products.
        """
        pass

    @abstractmethod
    def remove_product(self, product_id: str) -> None:
        """
        Remove a product from the repository by its ID.

        :param product_id: The ID of the product to remove.
        """
        pass

    @abstractmethod
    def get_product_by_id(self, product_id: str) -> Optional[_Product]:
        """
        Retrieve a product by its ID from the repository.

        :param product_id: The ID of the product to retrieve.
        :return: The retrieved product, or None if no product with the given ID exists.
        """
        pass

    @abstractmethod
    def update_product(self, product: _Product) -> None:
        """
        Update an existing product in the repository.

        :param product: The product with updated details.
        """
        pass
