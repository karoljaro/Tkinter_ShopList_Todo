import pytest
from pydantic import ValidationError
from src.application.dto.ProductDTO import ProductDTO


def test_valid_product_dto():
    product_dto = ProductDTO(name="Test Product", quantity=10)
    assert product_dto.name == "Test Product"
    assert product_dto.quantity == 10


def test_invalid_product_dto_empty_name():
    with pytest.raises(ValidationError, match="Product name cannot be empty"):
        ProductDTO(name="", quantity=10)


def test_invalid_product_dto_negative_quantity():
    with pytest.raises(ValidationError, match="Quantity must be positive"):
        ProductDTO(name="Test Product", quantity=-1)


def test_invalid_product_dto_non_integer_quantity():
    with pytest.raises(ValidationError, match="Input should be a valid integer"):
        ProductDTO(name="Test Product", quantity="ten")
