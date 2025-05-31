import pytest
from src.application.usecases.GetAllProducts import GetAllProducts
from src.infrastructure.InMemoryProductRepository import InMemoryProductRepository
from src.domain.Product_Entity import _Product


@pytest.fixture
def product_repository():
    return InMemoryProductRepository()


@pytest.fixture
def get_all_products_use_case(product_repository):
    return GetAllProducts(product_repository)


def test_get_all_products(get_all_products_use_case, product_repository):
    product1 = _Product(name="Test Product 1", quantity=10)
    product2 = _Product(name="Test Product 2", quantity=20)

    # Add products
    product_repository.add_product(product1)
    product_repository.add_product(product2)

    # Call the use case
    products = get_all_products_use_case.execute()

    # Assertions
    assert len(products) == 2
    assert products[0].name == "Test Product 1"
    assert products[0].quantity == 10
    assert products[1].name == "Test Product 2"
    assert products[1].quantity == 20


def test_get_all_products_empty_repository(get_all_products_use_case):
    # Call the use case
    products = get_all_products_use_case.execute()

    # Assertions
    assert len(products) == 0
