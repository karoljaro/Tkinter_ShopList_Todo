from src.application.usecases.AddProduct import AddProduct
from src.application.usecases.GetAllProducts import GetAllProducts
from src.application.usecases.GetProductById import GetProductById
from src.application.usecases.RemoveProduct import RemoveProduct
from src.application.usecases.UpdateProduct import UpdateProduct
from src.application.repositories.IProductRepository import IProductRepository
from src.application.dto.ProductDTO import ProductDTO
from src.utils.errorHandlerDecorator import handle_exceptions
from src.domain.Product_Entity import _Product
from src.infrastructure.InMemoryProductRepository import InMemoryProductRepository

class ProductController:
    def __init__(self, productRepository: IProductRepository = InMemoryProductRepository()):
        self.product_repository = productRepository
        self.add_product_use_case = AddProduct(self.product_repository)
        self.get_all_products_use_case = GetAllProducts(self.product_repository)
        self.get_product_by_id_use_case = GetProductById(self.product_repository)
        self.remove_product_use_case = RemoveProduct(self.product_repository)
        self.update_product_use_case = UpdateProduct(self.product_repository)

    @handle_exceptions
    def add_product(self, name: str, quantity: int, purchased: bool = False) -> _Product:
        product_dto = ProductDTO(name=name, quantity=quantity, purchased=purchased)
        return self.add_product_use_case.execute(product_dto)

    @handle_exceptions
    def get_all_products(self) -> list[_Product]:
        return self.get_all_products_use_case.execute()

    @handle_exceptions
    def get_product_by_id(self, product_id: str) -> _Product:
        return self.get_product_by_id_use_case.execute(product_id)

    @handle_exceptions
    def remove_product(self, product_id: str) -> None:
        self.remove_product_use_case.execute(product_id)

    @handle_exceptions
    def update_product(self, id: str, name: str, quantity: int, purchased: bool) -> _Product:
        product_dto = ProductDTO(id=id, name=name, quantity=quantity, purchased=purchased)
        return self.update_product_use_case.execute(product_dto)