import pytest
from unittest.mock import Mock
from src.infrastructure.database.PostgreSQLProductRepository import (
    PostgreSQLProductRepository,
)
from src.infrastructure.services.DatabaseService import DatabaseService
from src.domain.Product_Entity import _Product


class TestPostgreSQLProductRepository:
    """Integration tests for PostgreSQL Product Repository."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_db_service = Mock(spec=DatabaseService)
        self.repository = PostgreSQLProductRepository(self.mock_db_service)
        self.sample_product = _Product(
            id="test-id-123", name="Test Product", quantity=5, purchased=False
        )

    def test_add_product_success(self):
        """Test successful product addition."""
        # Mock that product doesn't exist yet (for duplicate check)
        self.mock_db_service.execute_query.return_value = (
            []
        )  # Mock successful database insertion
        self.mock_db_service.execute_command.return_value = 1

        # Execute
        self.repository.add_product(self.sample_product)

        # Verify
        self.mock_db_service.execute_command.assert_called_once()
        call_args = self.mock_db_service.execute_command.call_args
        assert "INSERT INTO products" in call_args[0][0]
        assert call_args[0][1]["id"] == "test-id-123"
        assert call_args[0][1]["name"] == "Test Product"

    def test_add_product_failure(self):
        """Test product addition failure handling."""
        # Mock that product doesn't exist yet (for duplicate check)
        self.mock_db_service.execute_query.return_value = []
        # Mock database error
        self.mock_db_service.execute_command.side_effect = Exception("Database error")

        # Execute and verify exception
        with pytest.raises(Exception, match="Database error"):
            self.repository.add_product(self.sample_product)

    def test_get_all_products_success(self):
        """Test successful retrieval of all products."""
        # Mock database response
        mock_rows = [
            {"id": "test-id-1", "name": "Product 1", "quantity": 3, "purchased": False},
            {"id": "test-id-2", "name": "Product 2", "quantity": 7, "purchased": True},
        ]
        self.mock_db_service.execute_query.return_value = mock_rows

        # Execute
        products = self.repository.get_all_products()

        # Verify
        assert len(products) == 2
        assert products[0].name == "Product 1"
        assert products[0].quantity == 3
        assert products[0].purchased is False
        assert products[1].name == "Product 2"
        assert products[1].purchased is True

    def test_get_all_products_empty(self):
        """Test retrieval when no products exist."""
        # Mock empty database response
        self.mock_db_service.execute_query.return_value = []

        # Execute
        products = self.repository.get_all_products()

        # Verify
        assert len(products) == 0
        assert products == []

    def test_get_product_by_id_found(self):
        """Test successful product retrieval by ID."""
        # Mock database response
        mock_row = {
            "id": "test-id-123",
            "name": "Found Product",
            "quantity": 10,
            "purchased": True,
        }
        self.mock_db_service.execute_query.return_value = [mock_row]

        # Execute
        product = self.repository.get_product_by_id("test-id-123")

        # Verify
        assert product is not None
        assert product.id == "test-id-123"
        assert product.name == "Found Product"
        assert product.quantity == 10
        assert product.purchased is True

    def test_get_product_by_id_not_found(self):
        """Test product retrieval when ID doesn't exist."""
        # Mock empty database response
        self.mock_db_service.execute_query.return_value = []

        # Execute
        product = self.repository.get_product_by_id("non-existent-id")

        # Verify
        assert product is None

    def test_update_product_success(self):
        """Test successful product update."""
        # Mock that product exists (for existence check)
        mock_existing_row = {
            "id": "test-id-123",
            "name": "Test Product",
            "quantity": 5,
            "purchased": False,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00",
        }
        self.mock_db_service.execute_query.return_value = [
            mock_existing_row
        ]  # Mock successful database update
        self.mock_db_service.execute_command.return_value = 1

        # Execute
        self.repository.update_product(self.sample_product)

        # Verify
        # Should be called twice: once for existence check, once for update
        assert self.mock_db_service.execute_command.call_count == 1
        call_args = self.mock_db_service.execute_command.call_args
        assert "UPDATE products" in call_args[0][0]
        assert call_args[0][1]["id"] == "test-id-123"

    def test_update_product_not_found(self):
        """Test update when product doesn't exist."""
        # Mock that product doesn't exist (for existence check)
        self.mock_db_service.execute_query.return_value = []
        # Mock no rows affected        self.mock_db_service.execute_command.return_value = 0

        # Execute and verify exception
        with pytest.raises(
            ValueError, match="Product with id test-id-123 does not exist"
        ):
            self.repository.update_product(self.sample_product)

    def test_remove_product_success(self):
        """Test successful product removal."""
        # Mock that product exists (for existence check)
        mock_existing_row = {
            "id": "test-id-123",
            "name": "Test Product",
            "quantity": 5,
            "purchased": False,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00",
        }
        self.mock_db_service.execute_query.return_value = [mock_existing_row]
        # Mock successful database deletion
        self.mock_db_service.execute_command.return_value = 1
        # Execute
        self.repository.remove_product("test-id-123")

        # Verify
        assert self.mock_db_service.execute_command.call_count == 1
        call_args = self.mock_db_service.execute_command.call_args
        assert "DELETE FROM products WHERE id" in call_args[0][0]
        assert call_args[0][1]["product_id"] == "test-id-123"

    def test_remove_product_not_found(self):
        """Test removal when product doesn't exist."""
        # Mock that product doesn't exist (for existence check)
        self.mock_db_service.execute_query.return_value = []
        # Mock no rows affected        self.mock_db_service.execute_command.return_value = 0

        # Execute and verify exception
        with pytest.raises(
            ValueError, match="Product with id non-existent does not exist"
        ):
            self.repository.remove_product("non-existent")


@pytest.mark.integration
class TestPostgreSQLIntegration:
    """Integration tests requiring actual PostgreSQL database."""

    @pytest.fixture(autouse=True)
    def setup_database(self):
        """Setup test database if available."""
        # Skip integration tests if PostgreSQL is not available
        try:
            from src.infrastructure.services.DatabaseService import DatabaseService

            db_service = DatabaseService()
            if not db_service.health_check():
                pytest.skip("PostgreSQL not available for integration tests")

            # Initialize schema for tests
            db_service.initialize_schema()
            self.db_service = db_service
            self.repository = PostgreSQLProductRepository(db_service)

        except Exception as e:
            pytest.skip(f"PostgreSQL setup failed: {str(e)}")

    def test_full_product_lifecycle(self):
        """Test complete product lifecycle: create, read, update, delete."""
        # Create test product
        product = _Product(
            name="Integration Test Product", quantity=15, purchased=False
        )

        # Add product
        self.repository.add_product(product)

        # Verify it was added
        retrieved = self.repository.get_product_by_id(product.id)
        assert retrieved is not None
        assert retrieved.name == "Integration Test Product"
        assert retrieved.quantity == 15
        assert retrieved.purchased is False

        # Update product
        product.quantity = 20
        product.purchased = True
        self.repository.update_product(product)

        # Verify update
        updated = self.repository.get_product_by_id(product.id)
        assert updated.quantity == 20
        assert updated.purchased is True

        # Remove product
        self.repository.remove_product(product.id)

        # Verify removal
        removed = self.repository.get_product_by_id(product.id)
        assert removed is None
