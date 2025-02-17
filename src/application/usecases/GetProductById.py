from src.application.repositories.IProductRepository import IProductRepository
from src.domain.Product_Entity import _Product

class GetProductById:
    def __init__(self, productRepository: IProductRepository):
        self.__productRepository = productRepository

    def execute(self, id: str) -> _Product:
        product = self.__productRepository.get_product_by_id(id)
        if product is None:
            raise ValueError(f"Product with id {id} does not exist.")
        return product