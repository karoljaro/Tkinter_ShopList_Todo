from typing import List, Optional
from src.application.repositories.IProductRepository import IProductRepository
from src.domain.Product_Entity import _Product
from src.infrastructure.services.DatabaseService import DatabaseService
from src.infrastructure.mappers.ProductMapper import ProductMapper
from src.utils.errorHandlerDecorator import handle_exceptions


class PostgreSQLProductRepository(IProductRepository):
    """
    PostgreSQL-based implementation of the IProductRepository interface.
    Uses Clean Architecture principles with proper layer separation.
    """

    def __init__(self, database_service: Optional[DatabaseService] = None):
        """
        Initialize the PostgreSQL repository.

        :param database_service: Optional database service instance
        """
        self._db_service = database_service or DatabaseService()
        self._mapper = ProductMapper()
        self._ensure_schema_initialized()

    def _ensure_schema_initialized(self) -> None:
        """Ensure database schema is properly initialized."""
        try:
            self._db_service.initialize_schema()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize database schema: {e}")

    @handle_exceptions
    def add_product(self, product: _Product) -> _Product:
        """
        Add a new product to the PostgreSQL database.

        :param product: The product to add
        :return: The added product
        :raises ValueError: If a product with the same ID already exists
        """
        # Validate product for persistence
        validation_errors = self._mapper.validate_for_persistence(product)
        if validation_errors:
            raise ValueError(
                f"Product validation failed: {', '.join(validation_errors)}"
            )

        # Check if product already exists
        if self.get_product_by_id(product.id) is not None:
            raise ValueError(f"Product with id {product.id} already exists.")

        # Insert product
        product_data = self._mapper.to_db_row(product)
        insert_sql = """
        INSERT INTO products (id, name, quantity, purchased)
        VALUES (%(id)s, %(name)s, %(quantity)s, %(purchased)s)
        """

        affected_rows = self._db_service.execute_command(insert_sql, product_data)
        if affected_rows != 1:
            raise RuntimeError(
                f"Expected to insert 1 row, but {affected_rows} were affected"
            )

        return product

    @handle_exceptions
    def get_all_products(self) -> List[_Product]:
        """
        Retrieve all products from the PostgreSQL database.

        :return: A list of all products
        """
        select_sql = """
        SELECT id, name, quantity, purchased, created_at, updated_at
        FROM products
        ORDER BY created_at DESC
        """

        rows = self._db_service.execute_query(select_sql)
        return [self._mapper.from_db_row(row) for row in rows]

    @handle_exceptions
    def remove_product(self, product_id: str) -> None:
        """
        Remove a product from the PostgreSQL database by its ID.

        :param product_id: The ID of the product to remove
        :raises ValueError: If no product with the given ID exists
        """
        # Verify product exists
        if self.get_product_by_id(product_id) is None:
            raise ValueError(f"Product with id {product_id} does not exist.")

        delete_sql = """
        DELETE FROM products WHERE id = %(product_id)s
        """

        affected_rows = self._db_service.execute_command(
            delete_sql, {"product_id": product_id}
        )

        if affected_rows != 1:
            raise RuntimeError(
                f"Expected to delete 1 row, but {affected_rows} were affected"
            )

    @handle_exceptions
    def get_product_by_id(self, product_id: str) -> Optional[_Product]:
        """
        Retrieve a product by its ID from the PostgreSQL database.

        :param product_id: The ID of the product to retrieve
        :return: The retrieved product, or None if no product with the given ID exists
        """
        select_sql = """
        SELECT id, name, quantity, purchased, created_at, updated_at
        FROM products
        WHERE id = %(product_id)s
        """

        rows = self._db_service.execute_query(select_sql, {"product_id": product_id})

        if not rows:
            return None

        return self._mapper.from_db_row(rows[0])

    @handle_exceptions
    def update_product(self, product: _Product) -> _Product:
        """
        Update an existing product in the PostgreSQL database.

        :param product: The product with updated details
        :return: The updated product
        :raises ValueError: If no product with the given ID exists
        """
        # Validate product for persistence
        validation_errors = self._mapper.validate_for_persistence(product)
        if validation_errors:
            raise ValueError(
                f"Product validation failed: {', '.join(validation_errors)}"
            )

        # Check if product exists
        if self.get_product_by_id(product.id) is None:
            raise ValueError(f"Product with id {product.id} does not exist.")

        # Update product
        product_data = self._mapper.to_db_row(product)
        update_sql = """
        UPDATE products 
        SET name = %(name)s, 
            quantity = %(quantity)s, 
            purchased = %(purchased)s,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %(id)s
        """

        affected_rows = self._db_service.execute_command(update_sql, product_data)
        if affected_rows != 1:
            raise RuntimeError(
                f"Expected to update 1 row, but {affected_rows} were affected"
            )

        return product

    def health_check(self) -> bool:
        """
        Check if the PostgreSQL database connection is healthy.

        :return: True if database is accessible and schema is valid
        """
        return self._db_service.health_check()

    def get_products_by_purchase_status(self, purchased: bool) -> List[_Product]:
        """
        Get products filtered by purchase status.

        :param purchased: Purchase status to filter by
        :return: List of products matching the status
        """
        select_sql = """
        SELECT id, name, quantity, purchased, created_at, updated_at
        FROM products
        WHERE purchased = %(purchased)s
        ORDER BY created_at DESC
        """

        rows = self._db_service.execute_query(select_sql, {"purchased": purchased})

        return [self._mapper.from_db_row(row) for row in rows]

    def get_product_count(self) -> int:
        """
        Get the total number of products in the database.

        :return: Total product count
        """
        count_sql = "SELECT COUNT(*) as count FROM products"

        rows = self._db_service.execute_query(count_sql)
        return rows[0]["count"] if rows else 0

    def close(self):
        """Close database connections and cleanup resources."""
        pass
