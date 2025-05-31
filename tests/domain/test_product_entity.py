import pytest
from src.domain.Product_Entity import _Product


@pytest.fixture
def product():
    return _Product(name="Test Product", quantity=10)


def test_initial_state(product):
    assert product.name == "Test Product"
    assert product.quantity == 10
    assert not product.purchased


def test_set_purchased(product):
    product.purchased = True
    assert product.purchased
    product.purchased = False
    assert not product.purchased


def test_generate_uuid():
    product = _Product(name="Test Product", quantity=10)
    assert product.id is not None
    assert len(product.id) > 0


def test_set_existing_id():
    existing_id = "existing-id"
    product = _Product(name="Test Product", quantity=10, id=existing_id)
    assert product.id == existing_id


def test_quantity_must_be_positive():
    with pytest.raises(ValueError, match="Quantity must be a positive integer."):
        _Product(name="Test Product", quantity=-1)


def test_name_must_not_be_empty():
    with pytest.raises(ValueError, match="Product name cannot be empty."):
        _Product(name="", quantity=10)
