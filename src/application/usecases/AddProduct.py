from src.application.repositories.IProductRepository import IProductRepository
from src.domain.Product_Entity import _Product
from src.application.dto.ProductDTO import ProductDTO

class AddProduct:
    """
    Use case for adding a new product to the repository.
    """
    def __init__(self, productRepository: IProductRepository):
        """
        Initialize the AddProduct use case with a product repository.

        :param productRepository: An instance of IProductRepository.
        """
        self.__productRepository = productRepository

    def execute(self, product_dto: ProductDTO) -> _Product:
        """
        Execute the use case to add a new product.

        :param product_dto: Data transfer object containing product details.
        :return: The added product.
        :raises ValueError: If a product with the same ID already exists.
        """
        if product_dto.id and self.__productRepository.get_product_by_id(product_dto.id):
            raise ValueError(f"Product with id {product_dto.id} already exists.")
        product = _Product(
            id=product_dto.id,
            name=product_dto.name,
            quantity=product_dto.quantity,
            purchased=bool(product_dto.purchased)
        )
        self.__productRepository.add_product(product)
        return product