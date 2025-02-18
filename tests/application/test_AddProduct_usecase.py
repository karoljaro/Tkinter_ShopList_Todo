import pytest
from src.application.usecases.AddProduct import AddProduct
from src.infrastructure.InMemoryProductRepository import InMemoryProductRepository
from src.application.dto.ProductDTO import ProductDTO

@pytest.fixture
def product_repository():
    return InMemoryProductRepository()

@pytest.fixture
def add_product_use_case(product_repository):
    return AddProduct(product_repository)

def test_add_product(add_product_use_case, product_repository):
    name = "Test Product"
    quantity = 10
    product_dto = ProductDTO(name=name, quantity=quantity)

    # Call the use case
    product = add_product_use_case.execute(product_dto)

    # Assertions
    assert product.name == name
    assert product.quantity == quantity
    assert product_repository.get_product_by_id(product.id) is not None

def test_add_product_increases_repository_size(add_product_use_case, product_repository):
    initial_size = len(product_repository.get_all_products())
    product_dto = ProductDTO(name="Test Product", quantity=10)
    add_product_use_case.execute(product_dto)
    new_size = len(product_repository.get_all_products())
    
    assert new_size == initial_size + 1

def test_add_product_with_existing_id(add_product_use_case, product_repository):
    product_dto = ProductDTO(id="existing_id", name="Test Product", quantity=10)
    product = add_product_use_case.execute(product_dto)
    
    with pytest.raises(ValueError, match=f"Product with id {product_dto.id} already exists."):
        add_product_use_case.execute(product_dto)