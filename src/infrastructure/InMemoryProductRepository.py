from src.application.repositories.IProductRepository import IProductRepository
from src.domain.Product_Entity import _Product
from src.utils.errorHandlerDecorator import handle_exceptions
from typing import List, Optional


class InMemoryProductRepository(IProductRepository):
    """
    In-memory implementation of the IProductRepository interface.
    """

    def __init__(self) -> None:
        """
        Initialize the repository with an empty list of products.
        """
        self.__products: List[_Product] = []

    @handle_exceptions
    def add_product(self, product: _Product) -> _Product:
        """
        Add a new product to the repository.

        :param product: The product to add.
        :return: The added product.
        :raises ValueError: If a product with the same ID already exists.
        """
        if self.get_product_by_id(product.id) is not None:
            raise ValueError(f"Product with id {product.id} already exists.")
        self.__products.append(product)
        return product

    @handle_exceptions
    def get_all_products(self) -> List[_Product]:
        """
        Retrieve all products from the repository.

        :return: A list of all products.
        """
        return self.__products

    @handle_exceptions
    def remove_product(self, product_id: str) -> None:
        """
        Remove a product from the repository by its ID.

        :param product_id: The ID of the product to remove.
        :raises ValueError: If no product with the given ID exists.
        """
        product = self.get_product_by_id(product_id)
        if product is None:
            raise ValueError(f"Product with id {product_id} does not exist.")
        self.__products = [
            product for product in self.__products if product.id != product_id
        ]

    @handle_exceptions
    def get_product_by_id(self, product_id: str) -> Optional[_Product]:
        """
        Retrieve a product by its ID from the repository.

        :param product_id: The ID of the product to retrieve.
        :return: The retrieved product, or None if no product with the given ID exists.
        """
        for product in self.__products:
            if product.id == product_id:
                return product
        return None

    @handle_exceptions
    def update_product(self, product: _Product) -> _Product:
        """
        Update an existing product in the repository.

        :param product: The product with updated details.
        :return: The updated product.
        :raises ValueError: If no product with the given ID exists.
        """
        for i, p in enumerate(self.__products):
            if p.id == product.id:
                self.__products[i] = product
                return product
        raise ValueError(f"Product with id {product.id} does not exist.")
