import pytest
from src.infrastructure.JsonProductRepository import JsonProductRepository
from src.domain.Product_Entity import _Product

@pytest.fixture
def product_repository(tmp_path):
    file_path = tmp_path / "products.json"
    return JsonProductRepository(file_path)

def test_add_product(product_repository):
    product = _Product(name="Test Product", quantity=10, purchased=True)
    product_repository.add_product(product)
    
    assert product_repository.get_product_by_id(product.id) is not None
    assert product_repository.get_product_by_id(product.id).name == "Test Product"
    assert product_repository.get_product_by_id(product.id).quantity == 10
    assert product_repository.get_product_by_id(product.id).purchased == True

def test_add_product_with_existing_id(product_repository):
    product1 = _Product(name="Test Product 1", quantity=10, purchased=True)
    product2 = _Product(name="Test Product 2", quantity=20, id=product1.id)
    
    product_repository.add_product(product1)
    
    with pytest.raises(ValueError, match=f"Product with id {product1.id} already exists."):
        product_repository.add_product(product2)

def test_get_all_products(product_repository):
    product1 = _Product(name="Test Product 1", quantity=10, purchased=True)
    product2 = _Product(name="Test Product 2", quantity=20, purchased=False)
    
    product_repository.add_product(product1)
    product_repository.add_product(product2)
    
    products = product_repository.get_all_products()
    
    assert len(products) == 2
    assert products[0].name == "Test Product 1"
    assert products[0].quantity == 10
    assert products[0].purchased == True
    assert products[1].name == "Test Product 2"
    assert products[1].quantity == 20
    assert products[1].purchased == False

def test_remove_product(product_repository):
    product = _Product(name="Test Product", quantity=10, purchased=True)
    product_repository.add_product(product)
    
    # Remove the product
    product_repository.remove_product(product.id)
    
    # Assertions
    assert product_repository.get_product_by_id(product.id) is None

def test_remove_nonexistent_product(product_repository):
    with pytest.raises(ValueError, match="Product with id nonexistent_id does not exist."):
        product_repository.remove_product("nonexistent_id")

def test_get_product_by_id(product_repository):
    product = _Product(name="Test Product", quantity=10, purchased=True)
    product_repository.add_product(product)
    
    # Call the method
    retrieved_product = product_repository.get_product_by_id(product.id)
    
    # Assertions
    assert retrieved_product is not None
    assert retrieved_product.name == "Test Product"
    assert retrieved_product.quantity == 10
    assert retrieved_product.purchased == True

def test_get_product_by_nonexistent_id(product_repository):
    assert product_repository.get_product_by_id("nonexistent_id") is None

def test_update_product(product_repository):
    product = _Product(name="Test Product", quantity=10, purchased=True)
    product_repository.add_product(product)
    
    # Update the product
    updated_product = _Product(name="Updated Product", quantity=20, id=product.id, purchased=False)
    product_repository.update_product(updated_product)
    
    # Assertions
    retrieved_product = product_repository.get_product_by_id(product.id)
    assert retrieved_product is not None
    assert retrieved_product.name == "Updated Product"
    assert retrieved_product.quantity == 20
    assert retrieved_product.purchased == False

def test_update_nonexistent_product(product_repository):
    product = _Product(name="Nonexistent Product", quantity=10, id="nonexistent_id", purchased=True)
    with pytest.raises(ValueError, match="Product with id nonexistent_id does not exist."):
        product_repository.update_product(product)