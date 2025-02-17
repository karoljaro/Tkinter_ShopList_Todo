from src.application.repositories.IProductRepository import IProductRepository
from src.domain.Product_Entity import _Product
from typing import List

class GetAllProducts: 
    def __init__(self, productRepository: IProductRepository):
        self.__productRepository = productRepository

    def execute(self) -> List[_Product]:
        products = self.__productRepository.get_all_products()
        return products
