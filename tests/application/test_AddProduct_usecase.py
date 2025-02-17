import pytest
from src.application.usecases.AddProduct import AddProduct
from src.infrastructure.InMemoryProductRepository import InMemoryProductRepository

@pytest.fixture
def product_repository():
    return InMemoryProductRepository()

@pytest.fixture
def add_product_use_case(product_repository):
    return AddProduct(product_repository)

def test_add_product(add_product_use_case, product_repository):
    name = "Test Product"
    quantity = 10

    # Call the use case
    product = add_product_use_case.execute(name, quantity)

    # Assertions
    assert product.name == name
    assert product.quantity == quantity
    assert product_repository.get_product_by_id(product.id) is not None

def test_add_product_increases_repository_size(add_product_use_case, product_repository):
    initial_size = len(product_repository.get_all_products())
    add_product_use_case.execute("Test Product", 10)
    new_size = len(product_repository.get_all_products())
    
    assert new_size == initial_size + 1