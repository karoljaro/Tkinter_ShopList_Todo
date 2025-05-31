from src.application.repositories.IProductRepository import IProductRepository
from src.domain.Product_Entity import _Product


class GetProductById:
    """
    Use case for retrieving a product by its ID from the repository.
    """

    def __init__(self, productRepository: IProductRepository):
        """
        Initialize the GetProductById use case with a product repository.

        :param productRepository: An instance of IProductRepository.
        """
        self.__productRepository = productRepository

    def execute(self, id: str) -> _Product:
        """
        Execute the use case to retrieve a product by its ID.

        :param id: The ID of the product to retrieve.
        :return: The retrieved product.
        :raises ValueError: If no product with the given ID exists.
        """
        product = self.__productRepository.get_product_by_id(id)
        if product is None:
            raise ValueError(f"Product with id {id} does not exist.")
        return product
