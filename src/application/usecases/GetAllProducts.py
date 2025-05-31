from src.application.repositories.IProductRepository import IProductRepository
from src.domain.Product_Entity import _Product
from typing import List


class GetAllProducts:
    """
    Use case for retrieving all products from the repository.
    """

    def __init__(self, productRepository: IProductRepository):
        """
        Initialize the GetAllProducts use case with a product repository.

        :param productRepository: An instance of IProductRepository.
        """
        self.__productRepository = productRepository

    def execute(self) -> List[_Product]:
        """
        Execute the use case to retrieve all products.

        :return: A list of all products.
        """
        products = self.__productRepository.get_all_products()
        return products
