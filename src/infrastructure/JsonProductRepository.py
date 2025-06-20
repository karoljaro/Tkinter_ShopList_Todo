from src.domain.Product_Entity import _Product
from src.application.repositories.IProductRepository import IProductRepository
from src.utils.errorHandlerDecorator import handle_exceptions
from typing import Optional
import json
import os


class JsonProductRepository(IProductRepository):
    """
    JSON-based implementation of the IProductRepository interface.
    """

    def __init__(self, file_path: str) -> None:
        """
        Initialize the repository with the given file path.

        :param file_path: Path to the JSON file storing product data.
        """
        self.file_path = os.path.abspath(file_path)
        self.__ensure_file_exists()
        self.__load_products()

    def __ensure_file_exists(self) -> None:
        """
        Ensure the JSON file exists. If not, create an empty file.
        """
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as file:
                json.dump([], file)

    def __load_products(self) -> None:
        """
        Load products from the JSON file into the repository.
        """
        try:
            with open(self.file_path, "r") as file:
                products_data = json.load(file)
                self.__products = []
                for data in products_data:
                    product = _Product(
                        id=data["id"],
                        name=data["name"],
                        quantity=data["quantity"],
                        purchased=data.get("purchased", False),
                    )
                    self.__products.append(product)
        except FileNotFoundError:
            self.__products = []

    def __save_products(self) -> None:
        """
        Save the current list of products to the JSON file.
        """
        with open(self.file_path, "w") as file:
            json.dump([product.__dict__ for product in self.__products], file)

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
        self.__save_products()
        return product

    @handle_exceptions
    def get_all_products(self) -> list[_Product]:
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
        self.__save_products()

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
        existing_product = self.get_product_by_id(product.id)
        if existing_product is None:
            raise ValueError(f"Product with id {product.id} does not exist.")
        existing_product.name = product.name
        existing_product.quantity = product.quantity
        existing_product.purchased = product.purchased
        self.__save_products()
        return existing_product

    @handle_exceptions
    def get_products_by_status_generator(self, purchased: bool):
        """
        Generator that yields products by purchase status.

        :param purchased: Purchase status to filter by.
        :yield: Products matching the purchase status.
        """
        for product in self.__products:
            if product.purchased == purchased:
                yield product

    @handle_exceptions
    def batch_products_generator(self, batch_size: int = 5):
        """
        Generator that yields products in batches.

        :param batch_size: Size of each batch.
        :yield: Batches of products.
        """
        for i in range(0, len(self.__products), batch_size):
            yield self.__products[i : i + batch_size]

    @handle_exceptions
    def get_products_with_name_length_range(
        self, min_length: int, max_length: int
    ) -> list[_Product]:
        """
        Get products with name length in specified range using list comprehension.

        :param min_length: Minimum name length.
        :param max_length: Maximum name length.
        :return: List of products with names in the specified length range.
        """
        return [
            product
            for product in self.__products
            if min_length <= len(product.name) <= max_length
        ]
