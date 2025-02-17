import pytest
from src.domain.Product_Entity import _Product
from src.infrastructure.InMemoryProductRepository import InMemoryProductRepository

@pytest.fixture
def product_repository():
    return InMemoryProductRepository()

def test_add_product(product_repository):
    product = _Product(name="Test Product", quantity=10)
    
    product_repository.add_product(product)
    
    assert product_repository.get_product_by_id(product.id) is not None
    assert product_repository.get_product_by_id(product.id).name == "Test Product"
    assert product_repository.get_product_by_id(product.id).quantity == 10

def test_add_product_with_existing_id(product_repository):
    product1 = _Product(name="Test Product 1", quantity=10)
    product2 = _Product(name="Test Product 2", quantity=20, id=product1.id)
    
    product_repository.add_product(product1)
    
    with pytest.raises(ValueError, match=f"Product with id {product1.id} already exists."):
        product_repository.add_product(product2)

def test_get_all_products(product_repository):
    product1 = _Product(name="Test Product 1", quantity=10)
    product2 = _Product(name="Test Product 2", quantity=20)
    
    product_repository.add_product(product1)
    product_repository.add_product(product2)
    
    products = product_repository.get_all_products()
    
    assert len(products) == 2
    assert products[0].name == "Test Product 1"
    assert products[0].quantity == 10
    assert products[1].name == "Test Product 2"
    assert products[1].quantity == 20

def test_remove_product(product_repository):
    product = _Product(name="Test Product", quantity=10)
    product_repository.add_product(product)
    
    # Remove the product
    product_repository.remove_product(product.id)
    
    # Assertions
    assert product_repository.get_product_by_id(product.id) is None

def test_remove_nonexistent_product(product_repository):
    with pytest.raises(ValueError, match="Product with id nonexistent_id does not exist."):
        product_repository.remove_product("nonexistent_id")

def test_get_product_by_id(product_repository):
    product = _Product(name="Test Product", quantity=10)
    product_repository.add_product(product)
    
    # Call the method
    retrieved_product = product_repository.get_product_by_id(product.id)
    
    # Assertions
    assert retrieved_product is not None
    assert retrieved_product.name == "Test Product"
    assert retrieved_product.quantity == 10

def test_get_product_by_nonexistent_id(product_repository):
    assert product_repository.get_product_by_id("nonexistent_id") is None

def test_update_product(product_repository):
    product = _Product(name="Test Product", quantity=10)
    product_repository.add_product(product)
    
    # Update the product
    updated_product = _Product(name="Updated Product", quantity=20, id=product.id)
    product_repository.update_product(updated_product)
    
    # Assertions
    retrieved_product = product_repository.get_product_by_id(product.id)
    assert retrieved_product is not None
    assert retrieved_product.name == "Updated Product"
    assert retrieved_product.quantity == 20

def test_update_nonexistent_product(product_repository):
    product = _Product(name="Nonexistent Product", quantity=10, id="nonexistent_id")
    with pytest.raises(ValueError, match="Product with id nonexistent_id does not exist."):
        product_repository.update_product(product)