import pytest
from infrastructure.repositories.in_memory_product_repository import InMemoryProductRepository
from domain.entities.product import Product
from typing import List

@pytest.fixture
def repository():
    return InMemoryProductRepository()

@pytest.fixture
def product():
    return Product(id=1, name="Apple", quantity=10)

def test_add_product(repository, product):
    repository.add_product(product)
    products = repository.get_all_products()
    assert len(product) == 1
    assert products[0].name == "Apple"
    assert products[0].quantity == 10

def test_remove_product(repository, product) -> None:
    repository.add_product(product)
    repository.remove_product(1)
    products: List[Product] = repository.get_all_products()
    assert len(products) == 0