import pytest
from src.application.usecases.RemoveProduct import RemoveProduct
from src.infrastructure.InMemoryProductRepository import InMemoryProductRepository
from src.domain.Product_Entity import _Product


@pytest.fixture
def product_repository():
    return InMemoryProductRepository()


@pytest.fixture
def remove_product_use_case(product_repository):
    return RemoveProduct(product_repository)


def test_remove_product(remove_product_use_case, product_repository):
    product = _Product(name="Test Product", quantity=10)
    product_repository.add_product(product)

    # Call the use case
    remove_product_use_case.execute(product.id)

    # Assertions
    assert product_repository.get_product_by_id(product.id) is None


def test_remove_nonexistent_product(remove_product_use_case):
    with pytest.raises(
        ValueError, match="Product with id nonexistent_id does not exist."
    ):
        remove_product_use_case.execute("nonexistent_id")
