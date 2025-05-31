import pytest
from src.application.usecases.UpdateProduct import UpdateProduct
from src.infrastructure.InMemoryProductRepository import InMemoryProductRepository
from src.application.dto.ProductDTO import ProductDTO
from src.domain.Product_Entity import _Product


@pytest.fixture
def product_repository():
    return InMemoryProductRepository()


@pytest.fixture
def update_product_use_case(product_repository):
    return UpdateProduct(product_repository)


def test_update_product(update_product_use_case, product_repository):
    product = _Product(name="Test Product", quantity=10)
    product_repository.add_product(product)

    product_dto = ProductDTO(
        id=product.id, name="Updated Product", quantity=20, purchased=True
    )
    updated_product = update_product_use_case.execute(product_dto)

    assert updated_product.name == "Updated Product"
    assert updated_product.quantity == 20
    assert updated_product.purchased


def test_update_nonexistent_product(update_product_use_case):
    product_dto = ProductDTO(
        id="nonexistent_id", name="Updated Product", quantity=20, purchased=True
    )
    with pytest.raises(
        ValueError, match="Product with id nonexistent_id does not exist."
    ):
        update_product_use_case.execute(product_dto)


def test_update_product_invalid_quantity(update_product_use_case, product_repository):
    product = _Product(name="Test Product", quantity=10)
    product_repository.add_product(product)

    with pytest.raises(ValueError, match="Quantity must be positive"):
        product_dto = ProductDTO(
            id=product.id, name="Updated Product", quantity=-1, purchased=True
        )
        update_product_use_case.execute(product_dto)


def test_update_product_empty_name(update_product_use_case, product_repository):
    product = _Product(name="Test Product", quantity=10)
    product_repository.add_product(product)

    with pytest.raises(ValueError, match="Product name cannot be empty."):
        product_dto = ProductDTO(id=product.id, name="", quantity=20, purchased=True)
        update_product_use_case.execute(product_dto)
