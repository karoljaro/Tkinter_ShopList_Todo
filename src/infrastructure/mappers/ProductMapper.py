from typing import Dict, List, Any
from src.domain.Product_Entity import _Product


class ProductMapper:
    """
    Infrastructure layer mapper for Product entity.
    Handles conversion between domain objects and external data formats.
    """

    @staticmethod
    def to_dict(product: _Product) -> Dict[str, Any]:
        """
        Convert Product entity to dictionary format.

        :param product: Product domain entity
        :return: Dictionary representation
        """
        return {
            "id": product.id,
            "name": product.name,
            "quantity": product.quantity,
            "purchased": product.purchased,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> _Product:
        """
        Create Product entity from dictionary.

        :param data: Dictionary with product data
        :return: Product domain entity
        """
        return _Product(
            id=data.get("id"),
            name=data["name"],
            quantity=data["quantity"],
            purchased=data.get("purchased", False),
        )

    @staticmethod
    def to_db_row(product: _Product) -> Dict[str, Any]:
        """
        Convert Product entity to database row format.

        :param product: Product domain entity
        :return: Dictionary for database insertion
        """
        return {
            "id": product.id,
            "name": product.name,
            "quantity": product.quantity,
            "purchased": product.purchased,
        }

    @staticmethod
    def from_db_row(row: Dict[str, Any]) -> _Product:
        """
        Create Product entity from database row.

        :param row: Database row as dictionary
        :return: Product domain entity
        """
        return _Product(
            id=row["id"],
            name=row["name"],
            quantity=row["quantity"],
            purchased=row["purchased"],
        )

    @staticmethod
    def validate_for_persistence(product: _Product) -> List[str]:
        """
        Validate product for database persistence.

        :param product: Product to validate
        :return: List of validation errors
        """
        errors = []

        if not product.id:
            errors.append("Product ID is required for persistence")

        if not product.name or not product.name.strip():
            errors.append("Product name cannot be empty")

        if not isinstance(product.quantity, int) or product.quantity <= 0:
            errors.append("Quantity must be a positive integer")

        if len(product.name) > 255:
            errors.append("Product name cannot exceed 255 characters")

        return errors
