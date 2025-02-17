from src.application.usecases.AddProduct import AddProduct
from src.application.usecases.GetAllProducts import GetAllProducts
from src.application.usecases.GetProductById import GetProductById
from src.application.usecases.RemoveProduct import RemoveProduct
from src.infrastructure.InMemoryProductRepository import InMemoryProductRepository
from src.application.repositories.IProductRepository import IProductRepository
from src.domain.Product_Entity import _Product

class ProductController:
    def __init__(self, productRepository: IProductRepository = InMemoryProductRepository()):
        self.product_repository = productRepository
        self.add_product_use_case = AddProduct(self.product_repository)
        self.get_all_products_use_case = GetAllProducts(self.product_repository)
        self.get_product_by_id_use_case = GetProductById(self.product_repository)
        self.remove_product_use_case = RemoveProduct(self.product_repository)

    def add_product(self, name: str, quantity: int) -> _Product:
        return self.add_product_use_case.execute(name, quantity)

    def get_all_products(self) -> list[_Product]:
        return self.get_all_products_use_case.execute()

    def get_product_by_id(self, product_id: str) -> _Product:
        return self.get_product_by_id_use_case.execute(product_id)

    def remove_product(self, product_id: str) -> None:
        self.remove_product_use_case.execute(product_id)