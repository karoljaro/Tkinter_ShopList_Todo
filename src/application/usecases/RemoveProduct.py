from src.application.repositories.IProductRepository import IProductRepository


class RemoveProduct:
    """
    Use case for removing a product from the repository.
    """

    def __init__(self, productRepository: IProductRepository):
        """
        Initialize the RemoveProduct use case with a product repository.

        :param productRepository: An instance of IProductRepository.
        """
        self.__productRepository = productRepository

    def execute(self, product_id: str) -> None:
        """
        Execute the use case to remove a product by its ID.

        :param product_id: The ID of the product to remove.
        :raises ValueError: If no product with the given ID exists.
        """
        product = self.__productRepository.get_product_by_id(product_id)
        if product is None:
            raise ValueError(f"Product with id {product_id} does not exist.")
        self.__productRepository.remove_product(product_id)
