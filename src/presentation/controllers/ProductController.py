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
    """
    Controller for managing products.
    """

    def __init__(
        self, productRepository: IProductRepository = InMemoryProductRepository()
    ):
        """
        Initialize the ProductController with a product repository and use cases.

        :param productRepository: An instance of IProductRepository. Defaults to InMemoryProductRepository.
        """
        self.product_repository = productRepository
        self.add_product_use_case = AddProduct(self.product_repository)
        self.get_all_products_use_case = GetAllProducts(self.product_repository)
        self.get_product_by_id_use_case = GetProductById(self.product_repository)
        self.remove_product_use_case = RemoveProduct(self.product_repository)
        self.update_product_use_case = UpdateProduct(self.product_repository)

    @handle_exceptions
    def add_product(
        self, name: str, quantity: int, purchased: bool = False
    ) -> _Product:
        """
        Add a new product.

        :param name: The name of the product.
        :param quantity: The quantity of the product.
        :param purchased: The purchase status of the product. Defaults to False.
        :return: The added product.
        """
        product_dto = ProductDTO(name=name, quantity=quantity, purchased=purchased)
        return self.add_product_use_case.execute(product_dto)

    @handle_exceptions
    def get_all_products(self) -> list[_Product]:
        """
        Retrieve all products.

        :return: A list of all products.
        """
        return self.get_all_products_use_case.execute()

    @handle_exceptions
    def get_product_by_id(self, product_id: str) -> _Product:
        """
        Retrieve a product by its ID.

        :param product_id: The ID of the product to retrieve.
        :return: The retrieved product.
        """
        return self.get_product_by_id_use_case.execute(product_id)

    @handle_exceptions
    def get_products_by_status(self, purchased: bool | None = None) -> list[_Product]:
        """
        Get products filtered by purchase status using list comprehension.

        :param purchased: Filter by purchase status (None for all, True for purchased, False for not purchased).
        :return: Filtered list of products.
        """
        products = self.get_all_products_use_case.execute()
        if purchased is None:
            return products
        return [product for product in products if product.purchased == purchased]

    @handle_exceptions
    def get_products_by_quantity_range(
        self, min_qty: int = 0, max_qty: int | None = None
    ) -> list[_Product]:
        """
        Get products within quantity range using list comprehension.

        :param min_qty: Minimum quantity (inclusive).
        :param max_qty: Maximum quantity (inclusive, None for no limit).
        :return: List of products within the quantity range.
        """
        products = self.get_all_products_use_case.execute()
        if max_qty is None:
            return [product for product in products if product.quantity >= min_qty]
        return [
            product for product in products if min_qty <= product.quantity <= max_qty
        ]

    @handle_exceptions
    def get_product_names_generator(self):
        """
        Generator that yields product names one by one.

        :yield: Product names.
        """
        products = self.get_all_products_use_case.execute()
        for product in products:
            yield product.name

    @handle_exceptions
    def search_products(self, search_term: str) -> list[_Product]:
        """
        Search products by name using list comprehension.

        :param search_term: Term to search for in product names.
        :return: List of products matching the search term.
        """
        products = self.get_all_products_use_case.execute()
        return [
            product
            for product in products
            if search_term.lower() in product.name.lower()
        ]

    @handle_exceptions
    def get_low_stock_products(self, threshold: int = 5) -> list[_Product]:
        """
        Get products with low stock using list comprehension.

        :param threshold: Quantity threshold for low stock.
        :return: List of products with quantity below threshold.
        """
        products = self.get_all_products_use_case.execute()
        return [product for product in products if product.quantity < threshold]

    @handle_exceptions
    def remove_product(self, product_id: str) -> None:
        """
        Remove a product by its ID.

        :param product_id: The ID of the product to remove.
        """
        self.remove_product_use_case.execute(product_id)

    @handle_exceptions
    def update_product(
        self, id: str, name: str, quantity: int, purchased: bool
    ) -> _Product:
        """
        Update an existing product.

        :param id: The ID of the product to update.
        :param name: The updated name of the product.
        :param quantity: The updated quantity of the product.
        :param purchased: The updated purchase status of the product.
        :return: The updated product.
        """
        product_dto = ProductDTO(
            id=id, name=name, quantity=quantity, purchased=purchased
        )
        return self.update_product_use_case.execute(product_dto)
