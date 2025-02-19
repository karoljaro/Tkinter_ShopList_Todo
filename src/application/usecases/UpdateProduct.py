from src.application.repositories.IProductRepository import IProductRepository
from src.domain.Product_Entity import _Product
from src.application.dto.ProductDTO import ProductDTO

class UpdateProduct:
    def __init__(self, productRepository: IProductRepository):
        self.__productRepository = productRepository

    def execute(self, product_dto: ProductDTO) -> _Product:
        existing_product = self.__productRepository.get_product_by_id(product_dto.id)
        if not existing_product:
            raise ValueError(f"Product with id {product_dto.id} does not exist.")
        
        # Update product fields
        existing_product.name = product_dto.name
        existing_product.quantity = product_dto.quantity
        existing_product.purchased = product_dto.purchased

        # Validate updated product
        if existing_product.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if not existing_product.name:
            raise ValueError("Product name cannot be empty.")

        self.__productRepository.update_product(existing_product)
        return existing_product