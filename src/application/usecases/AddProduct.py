from src.application.repositories.IProductRepository import IProductRepository
from src.domain.Product_Entity import _Product

class AddProduct:
    def __init__(self, productRepository: IProductRepository):
        self.__productRepository = productRepository

    def execute(self, name: str, quantity: int) -> _Product:
        product = _Product(name, quantity)
        self.__productRepository.add_product(product)
        return product