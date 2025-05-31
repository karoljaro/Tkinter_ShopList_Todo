import pytest
from src.infrastructure.JsonProductRepository import JsonProductRepository
from src.domain.Product_Entity import _Product
import json


@pytest.fixture
def product_repository(tmp_path):
    file_path = tmp_path / "products.json"
    return JsonProductRepository(file_path)


def test_ensure_file_exists(product_repository, tmp_path):
    file_path = tmp_path / "products.json"
    assert file_path.exists()


def test_load_products(product_repository, tmp_path):
    product = _Product(name="Test Product", quantity=10, purchased=True)
    product_repository.add_product(product)

    # Reinitialize the repository to simulate loading from file
    new_product_repository = JsonProductRepository(product_repository.file_path)

    assert len(new_product_repository.get_all_products()) == 1
    assert new_product_repository.get_all_products()[0].name == "Test Product"
    assert new_product_repository.get_all_products()[0].quantity == 10
    assert new_product_repository.get_all_products()[0].purchased == True


def test_save_products(product_repository):
    product = _Product(name="Test Product", quantity=10, purchased=True)
    product_repository.add_product(product)
    with open(product_repository.file_path, "r") as file:
        products_data = json.load(file)
    assert len(products_data) == 1
    assert products_data[0]["name"] == "Test Product"


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

    with pytest.raises(
        ValueError, match=f"Product with id {product1.id} already exists."
    ):
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
    with pytest.raises(
        ValueError, match="Product with id nonexistent_id does not exist."
    ):
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
    updated_product = _Product(
        name="Updated Product", quantity=20, id=product.id, purchased=False
    )
    product_repository.update_product(updated_product)

    # Assertions
    retrieved_product = product_repository.get_product_by_id(product.id)
    assert retrieved_product is not None
    assert retrieved_product.name == "Updated Product"
    assert retrieved_product.quantity == 20
    assert retrieved_product.purchased == False


def test_update_nonexistent_product(product_repository):
    product = _Product(
        name="Nonexistent Product", quantity=10, id="nonexistent_id", purchased=True
    )
    with pytest.raises(
        ValueError, match="Product with id nonexistent_id does not exist."
    ):
        product_repository.update_product(product)


def test_get_products_by_status_generator_purchased(product_repository):
    """Test generator for purchased products."""
    product1 = _Product(name="Product 1", quantity=10, purchased=True)
    product2 = _Product(name="Product 2", quantity=15, purchased=False)
    product3 = _Product(name="Product 3", quantity=5, purchased=True)

    product_repository.add_product(product1)
    product_repository.add_product(product2)
    product_repository.add_product(product3)

    purchased_generator = product_repository.get_products_by_status_generator(True)
    purchased_products = list(purchased_generator)

    assert len(purchased_products) == 2
    assert all(product.purchased for product in purchased_products)
    assert purchased_products[0].name == "Product 1"
    assert purchased_products[1].name == "Product 3"


def test_get_products_by_status_generator_not_purchased(product_repository):
    """Test generator for not purchased products."""
    product1 = _Product(name="Product 1", quantity=10, purchased=True)
    product2 = _Product(name="Product 2", quantity=15, purchased=False)
    product3 = _Product(name="Product 3", quantity=5, purchased=False)

    product_repository.add_product(product1)
    product_repository.add_product(product2)
    product_repository.add_product(product3)

    not_purchased_generator = product_repository.get_products_by_status_generator(False)
    not_purchased_products = list(not_purchased_generator)

    assert len(not_purchased_products) == 2
    assert all(not product.purchased for product in not_purchased_products)
    assert not_purchased_products[0].name == "Product 2"
    assert not_purchased_products[1].name == "Product 3"


def test_batch_products_generator_default_batch_size(product_repository):
    """Test batch generator with default batch size (5)."""
    products = []
    for i in range(7):
        product = _Product(name=f"Product {i+1}", quantity=10)
        products.append(product)
        product_repository.add_product(product)

    batch_generator = product_repository.batch_products_generator()
    batches = list(batch_generator)

    assert len(batches) == 2  # 7 products, batch size 5 -> 2 batches
    assert len(batches[0]) == 5
    assert len(batches[1]) == 2
    assert batches[0][0].name == "Product 1"
    assert batches[1][0].name == "Product 6"


def test_batch_products_generator_custom_batch_size(product_repository):
    """Test batch generator with custom batch size."""
    products = []
    for i in range(6):
        product = _Product(name=f"Product {i+1}", quantity=10)
        products.append(product)
        product_repository.add_product(product)

    batch_generator = product_repository.batch_products_generator(batch_size=3)
    batches = list(batch_generator)

    assert len(batches) == 2  # 6 products, batch size 3 -> 2 batches
    assert len(batches[0]) == 3
    assert len(batches[1]) == 3
    assert batches[0][0].name == "Product 1"
    assert batches[1][0].name == "Product 4"


def test_get_products_with_name_length_range(product_repository):
    """Test getting products with name length in specified range."""
    product1 = _Product(name="A", quantity=10)  # length 1
    product2 = _Product(name="Apple", quantity=15)  # length 5
    product3 = _Product(name="Banana Split", quantity=20)  # length 12
    product4 = _Product(name="Hi", quantity=5)  # length 2

    product_repository.add_product(product1)
    product_repository.add_product(product2)
    product_repository.add_product(product3)
    product_repository.add_product(product4)

    result = product_repository.get_products_with_name_length_range(2, 5)

    assert len(result) == 2
    assert all(2 <= len(product.name) <= 5 for product in result)
    names = [product.name for product in result]
    assert "Apple" in names
    assert "Hi" in names


def test_get_products_with_name_length_range_no_matches(product_repository):
    """Test getting products with name length range that has no matches."""
    product1 = _Product(name="A", quantity=10)  # length 1
    product2 = _Product(name="Very Long Product Name", quantity=15)  # length 23

    product_repository.add_product(product1)
    product_repository.add_product(product2)

    result = product_repository.get_products_with_name_length_range(5, 10)

    assert len(result) == 0


def test_generators_are_iterators(product_repository):
    """Test that generators return proper iterators."""
    product1 = _Product(name="Product 1", quantity=10, purchased=True)
    product2 = _Product(name="Product 2", quantity=15, purchased=False)

    product_repository.add_product(product1)
    product_repository.add_product(product2)

    # Test that generators return iterators
    status_gen = product_repository.get_products_by_status_generator(True)
    batch_gen = product_repository.batch_products_generator(batch_size=1)

    # Check they are generators/iterators
    assert hasattr(status_gen, "__iter__")
    assert hasattr(status_gen, "__next__")
    assert hasattr(batch_gen, "__iter__")
    assert hasattr(batch_gen, "__next__")

    # Test they can be iterated multiple times by creating new generators
    status_gen1 = product_repository.get_products_by_status_generator(True)
    status_gen2 = product_repository.get_products_by_status_generator(True)

    list1 = list(status_gen1)
    list2 = list(status_gen2)

    assert len(list1) == 1
    assert len(list2) == 1
    assert list1[0].name == list2[0].name
