import pytest
from src.domain.Product_Entity import _Product

@pytest.fixture
def product():
    return _Product(name="Test Product", quantity=10)

def test_initial_state(product):
    assert product.name == "Test Product"
    assert product.quantity == 10
    assert not product.purchased
    assert product.status == "niekupione"

def test_purchase(product):
    product.purchase()
    assert product.purchased
    assert product.status == "kupione"

def test_unpurchase(product):
    product.purchase()
    product.unpurchase()
    assert not product.purchased
    assert product.status == "niekupione"

def test_set_purchased(product):
    product.purchased = True
    assert product.purchased
    assert product.status == "kupione"
    product.purchased = False
    assert not product.purchased
    assert product.status == "niekupione"