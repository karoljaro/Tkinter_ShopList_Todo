import pytest
from src.presentation.controllers.ProductController import ProductController
from src.infrastructure.InMemoryProductRepository import InMemoryProductRepository
from src.domain.Product_Entity import _Product

@pytest.fixture
def product_repository():
    return InMemoryProductRepository()

@pytest.fixture
def product_controller(product_repository):
    return ProductController(product_repository)

def test_add_product(product_controller, product_repository):
    name = "Test Product"
    quantity = 10
    purchased = True
    
    # Call the method
    result = product_controller.add_product(name, quantity, purchased)
    
    # Assertions
    assert result.name == name
    assert result.quantity == quantity
    assert result.purchased == purchased
    assert product_repository.get_product_by_id(result.id) is not None

def test_get_all_products(product_controller, product_repository):
    product1 = _Product(name="Test Product 1", quantity=10)
    product2 = _Product(name="Test Product 2", quantity=20)
    
    # Add products directly to the repository
    product_repository.add_product(product1)
    product_repository.add_product(product2)
    
    # Call the method
    result = product_controller.get_all_products()
    
    # Assertions
    assert len(result) == 2
    assert result[0].name == "Test Product 1"
    assert result[0].quantity == 10
    assert result[1].name == "Test Product 2"
    assert result[1].quantity == 20

def test_get_product_by_id(product_controller, product_repository):
    product_id = "test_id"
    product = _Product(name="Test Product", quantity=10, id=product_id)
    
    # Add product directly to the repository
    product_repository.add_product(product)
    
    # Call the method
    result = product_controller.get_product_by_id(product_id)
    
    # Assertions
    assert result.id == product_id
    assert result.name == "Test Product"
    assert result.quantity == 10

def test_remove_product(product_controller, product_repository):
    product_id = "test_id"
    product = _Product(name="Test Product", quantity=10, id=product_id)
    
    # Add product directly to the repository
    product_repository.add_product(product)
    
    # Call the method
    product_controller.remove_product(product_id)
    
    # Assertions
    assert product_repository.get_product_by_id(product_id) is None

def test_update_product(product_controller, product_repository):
    product_id = "test_id"
    product = _Product(name="Test Product", quantity=10, id=product_id)
    
    # Add product directly to the repository
    product_repository.add_product(product)
    
    # Call the method
    updated_product = product_controller.update_product(product_id, "Updated Product", 20, False)
    
    # Assertions
    assert updated_product.name == "Updated Product"
    assert updated_product.quantity == 20
    assert not updated_product.purchased