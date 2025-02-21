from src.application.repositories.IProductRepository import IProductRepository
from src.domain.Product_Entity import _Product
from src.application.dto.ProductDTO import ProductDTO

class AddProduct:
    def __init__(self, productRepository: IProductRepository):
        self.__productRepository = productRepository

    def execute(self, product_dto: ProductDTO) -> _Product:
        if product_dto.id and self.__productRepository.get_product_by_id(product_dto.id):
            raise ValueError(f"Product with id {product_dto.id} already exists.")
        product = _Product(
            id=product_dto.id,
            name=product_dto.name,
            quantity=product_dto.quantity,
            purchased=product_dto.purchased
        )
        self.__productRepository.add_product(product)
        return product