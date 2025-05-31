import pytest
from src.application.usecases.GetProductById import GetProductById
from src.infrastructure.InMemoryProductRepository import InMemoryProductRepository
from src.domain.Product_Entity import _Product


@pytest.fixture
def product_repository():
    return InMemoryProductRepository()


@pytest.fixture
def get_product_by_id_use_case(product_repository):
    return GetProductById(product_repository)


def test_get_product_by_id(get_product_by_id_use_case, product_repository):
    product = _Product(name="Test Product", quantity=10)
    product_repository.add_product(product)

    # Call the use case
    retrieved_product = get_product_by_id_use_case.execute(product.id)

    # Assertions
    assert retrieved_product is not None
    assert retrieved_product.name == "Test Product"
    assert retrieved_product.quantity == 10


def test_get_product_by_nonexistent_id(get_product_by_id_use_case):
    with pytest.raises(
        ValueError, match="Product with id nonexistent_id does not exist."
    ):
        get_product_by_id_use_case.execute("nonexistent_id")
