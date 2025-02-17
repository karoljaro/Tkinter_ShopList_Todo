from src.application.repositories.IProductRepository import IProductRepository
from src.domain.Product_Entity import _Product

class RemoveProduct:
    def __init__(self, productRepository: IProductRepository):
        self.__productRepository = productRepository

    def execute(self, product_id: str) -> None:
        product = self.__productRepository.get_product_by_id(product_id)
        if product is None:
            raise ValueError(f"Product with id {product_id} does not exist.")
        self.__productRepository.remove_product(product_id)