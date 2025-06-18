from src.application.repositories.IProductRepository import IProductRepository
from src.domain.Product_Entity import _Product
from src.application.dto.ProductDTO import ProductDTO


class UpdateProduct:
    """
    Use case for updating an existing product in the repository.
    """

    def __init__(self, productRepository: IProductRepository):
        """
        Initialize the UpdateProduct use case with a product repository.

        :param productRepository: An instance of IProductRepository.
        """
        self.__productRepository = productRepository

    def execute(self, product_dto: ProductDTO) -> _Product:
        """
        Execute the use case to update an existing product.

        :param product_dto: Data transfer object containing updated product details.
        :return: The updated product.
        :raises ValueError: If no product with the given ID exists or if validation fails.
        """
        if product_dto.id is None:
            raise ValueError("Product ID is required for update operation.")

        existing_product = self.__productRepository.get_product_by_id(product_dto.id)
        if not existing_product:
            raise ValueError(f"Product with id {product_dto.id} does not exist.")

        existing_product.name = product_dto.name
        existing_product.quantity = product_dto.quantity
        existing_product.purchased = (
            product_dto.purchased if product_dto.purchased is not None else False
        )
        if existing_product.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if not existing_product.name:
            raise ValueError("Product name cannot be empty.")

        return self.__productRepository.update_product(existing_product)
