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

def test_get_products_by_status_all(product_controller, product_repository):
    """Test getting all products when purchased parameter is None."""
    product1 = _Product(name="Product 1", quantity=10, purchased=True)
    product2 = _Product(name="Product 2", quantity=15, purchased=False)
    product3 = _Product(name="Product 3", quantity=5, purchased=True)
    
    product_repository.add_product(product1)
    product_repository.add_product(product2)
    product_repository.add_product(product3)
    
    result = product_controller.get_products_by_status(None)
    
    assert len(result) == 3

def test_get_products_by_status_purchased(product_controller, product_repository):
    """Test getting only purchased products."""
    product1 = _Product(name="Product 1", quantity=10, purchased=True)
    product2 = _Product(name="Product 2", quantity=15, purchased=False)
    product3 = _Product(name="Product 3", quantity=5, purchased=True)
    
    product_repository.add_product(product1)
    product_repository.add_product(product2)
    product_repository.add_product(product3)
    
    result = product_controller.get_products_by_status(True)
    
    assert len(result) == 2
    assert all(product.purchased for product in result)
    assert result[0].name == "Product 1"
    assert result[1].name == "Product 3"

def test_get_products_by_status_not_purchased(product_controller, product_repository):
    """Test getting only not purchased products."""
    product1 = _Product(name="Product 1", quantity=10, purchased=True)
    product2 = _Product(name="Product 2", quantity=15, purchased=False)
    product3 = _Product(name="Product 3", quantity=5, purchased=False)
    
    product_repository.add_product(product1)
    product_repository.add_product(product2)
    product_repository.add_product(product3)
    
    result = product_controller.get_products_by_status(False)
    
    assert len(result) == 2
    assert all(not product.purchased for product in result)
    assert result[0].name == "Product 2"
    assert result[1].name == "Product 3"

def test_get_products_by_quantity_range_min_only(product_controller, product_repository):
    """Test getting products with minimum quantity only."""
    product1 = _Product(name="Product 1", quantity=5)
    product2 = _Product(name="Product 2", quantity=15)
    product3 = _Product(name="Product 3", quantity=25)
    
    product_repository.add_product(product1)
    product_repository.add_product(product2)
    product_repository.add_product(product3)
    
    result = product_controller.get_products_by_quantity_range(min_qty=10)
    
    assert len(result) == 2
    assert all(product.quantity >= 10 for product in result)
    assert result[0].name == "Product 2"
    assert result[1].name == "Product 3"

def test_get_products_by_quantity_range_min_max(product_controller, product_repository):
    """Test getting products within quantity range."""
    product1 = _Product(name="Product 1", quantity=5)
    product2 = _Product(name="Product 2", quantity=15)
    product3 = _Product(name="Product 3", quantity=25)
    
    product_repository.add_product(product1)
    product_repository.add_product(product2)
    product_repository.add_product(product3)
    
    result = product_controller.get_products_by_quantity_range(min_qty=10, max_qty=20)
    
    assert len(result) == 1
    assert result[0].quantity >= 10 and result[0].quantity <= 20
    assert result[0].name == "Product 2"

def test_get_product_names_generator(product_controller, product_repository):
    """Test getting product names generator."""
    product1 = _Product(name="Apple", quantity=5)
    product2 = _Product(name="Banana", quantity=15)
    product3 = _Product(name="Cherry", quantity=25)
    
    product_repository.add_product(product1)
    product_repository.add_product(product2)
    product_repository.add_product(product3)
    
    names_generator = product_controller.get_product_names_generator()
    names = list(names_generator)
    
    assert len(names) == 3
    assert "Apple" in names
    assert "Banana" in names
    assert "Cherry" in names

def test_search_products(product_controller, product_repository):
    """Test searching products by name."""
    product1 = _Product(name="Apple Juice", quantity=5)
    product2 = _Product(name="Banana Split", quantity=15)
    product3 = _Product(name="Apple Pie", quantity=25)
    product4 = _Product(name="Orange", quantity=10)
    
    product_repository.add_product(product1)
    product_repository.add_product(product2)
    product_repository.add_product(product3)
    product_repository.add_product(product4)
    
    result = product_controller.search_products("apple")
    
    assert len(result) == 2
    assert all("apple" in product.name.lower() for product in result)
    assert result[0].name == "Apple Juice"
    assert result[1].name == "Apple Pie"

def test_search_products_case_insensitive(product_controller, product_repository):
    """Test searching products case insensitive."""
    product1 = _Product(name="APPLE JUICE", quantity=5)
    product2 = _Product(name="banana split", quantity=15)
    
    product_repository.add_product(product1)
    product_repository.add_product(product2)
    
    result = product_controller.search_products("APple")
    
    assert len(result) == 1
    assert result[0].name == "APPLE JUICE"

def test_get_low_stock_products_default_threshold(product_controller, product_repository):
    """Test getting low stock products with default threshold (5)."""
    product1 = _Product(name="Product 1", quantity=3)
    product2 = _Product(name="Product 2", quantity=7)
    product3 = _Product(name="Product 3", quantity=1)
    product4 = _Product(name="Product 4", quantity=10)
    
    product_repository.add_product(product1)
    product_repository.add_product(product2)
    product_repository.add_product(product3)
    product_repository.add_product(product4)
    
    result = product_controller.get_low_stock_products()
    
    assert len(result) == 2
    assert all(product.quantity < 5 for product in result)
    assert result[0].name == "Product 1"
    assert result[1].name == "Product 3"

def test_get_low_stock_products_custom_threshold(product_controller, product_repository):
    """Test getting low stock products with custom threshold."""
    product1 = _Product(name="Product 1", quantity=8)
    product2 = _Product(name="Product 2", quantity=12)
    product3 = _Product(name="Product 3", quantity=5)
    
    product_repository.add_product(product1)
    product_repository.add_product(product2)
    product_repository.add_product(product3)
    
    result = product_controller.get_low_stock_products(threshold=10)
    
    assert len(result) == 2
    assert all(product.quantity < 10 for product in result)
    assert result[0].name == "Product 1"
    assert result[1].name == "Product 3"