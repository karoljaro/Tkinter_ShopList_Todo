import pytest
import os
from unittest.mock import patch, MagicMock
from src.infrastructure.services.DatabaseService import DatabaseService


class TestDatabaseService:
    """Unit tests for DatabaseService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.db_service = DatabaseService()

    def test_build_connection_string_defaults(self):
        """Test connection string building with default values."""
        with patch.dict(os.environ, {}, clear=True):
            db_service = DatabaseService()
            connection_string = db_service._build_connection_string()

            expected = (
                "postgresql://shoplist_user:shoplist_pass@localhost:5432/"
                "shoplist?connect_timeout=3"
            )
            assert connection_string == expected

    def test_build_connection_string_custom(self):
        """Test connection string building with custom environment variables."""
        env_vars = {
            "POSTGRES_HOST": "custom-host",
            "POSTGRES_PORT": "5433",
            "POSTGRES_DB": "custom_db",
            "POSTGRES_USER": "custom_user",
            "POSTGRES_PASSWORD": "custom_pass",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            db_service = DatabaseService()
            connection_string = db_service._build_connection_string()

            expected = (
                "postgresql://custom_user:custom_pass@custom-host:5433/"
                "custom_db?connect_timeout=3"
            )
            assert connection_string == expected

    @patch("src.infrastructure.services.DatabaseService.psycopg")
    def test_get_connection_success(self, mock_psycopg):
        """Test successful database connection."""
        # Mock connection
        mock_connection = MagicMock()
        mock_psycopg.connect.return_value = mock_connection

        # Execute
        with self.db_service.get_connection() as conn:
            assert conn == mock_connection

        # Verify connection was established and closed
        mock_psycopg.connect.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch("src.infrastructure.services.DatabaseService.psycopg")
    def test_get_connection_failure(self, mock_psycopg):
        """Test database connection failure."""
        # Mock connection failure
        mock_psycopg.connect.side_effect = Exception(
            "Connection failed"
        )  # Execute and verify exception
        with pytest.raises(Exception, match="Connection failed"):
            with self.db_service.get_connection():
                pass

    @patch("src.infrastructure.services.DatabaseService.psycopg")
    def test_get_transaction_success(self, mock_psycopg):
        """Test successful transaction handling."""
        # Mock connection and transaction
        mock_connection = MagicMock()
        mock_transaction = MagicMock()
        mock_connection.transaction.return_value.__enter__.return_value = (
            mock_transaction
        )
        mock_psycopg.connect.return_value = mock_connection

        # Execute
        with self.db_service.get_transaction() as conn:
            assert conn == mock_connection

        # Verify transaction was used
        mock_connection.transaction.assert_called_once()

    @patch("src.infrastructure.services.DatabaseService.psycopg")
    def test_get_transaction_rollback(self, mock_psycopg):
        """Test transaction rollback on exception."""
        # Mock connection
        mock_connection = MagicMock()
        mock_psycopg.connect.return_value = mock_connection

        # Mock transaction that raises exception
        mock_connection.transaction.return_value.__enter__.side_effect = Exception(
            "Transaction error"
        )  # Execute and verify exception propagation
        with pytest.raises(Exception, match="Transaction error"):
            with self.db_service.get_transaction():
                pass

    @patch("src.infrastructure.services.DatabaseService.psycopg")
    def test_health_check_healthy(self, mock_psycopg):
        """Test health check when database is healthy."""
        # Mock healthy database
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {"column": 1}
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_psycopg.connect.return_value = mock_connection

        # Execute
        is_healthy = self.db_service.health_check()  # Verify
        assert is_healthy is True
        mock_cursor.execute.assert_called_once_with("SELECT 1")

    @patch("src.infrastructure.services.DatabaseService.psycopg")
    def test_health_check_unhealthy(self, mock_psycopg):
        """Test health check when database is unhealthy."""
        # Mock database connection failure
        mock_psycopg.connect.side_effect = Exception("Connection failed")

        # Execute
        is_healthy = self.db_service.health_check()  # Verify
        assert is_healthy is False

    @patch("src.infrastructure.services.DatabaseService.psycopg")
    def test_initialize_schema(self, mock_psycopg):
        """Test schema initialization."""
        # Mock connection and cursor
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connection.transaction.return_value.__enter__.return_value = (
            mock_connection
        )
        mock_psycopg.connect.return_value = mock_connection

        # Execute
        self.db_service.initialize_schema()

        # Verify
        mock_cursor.execute.assert_called_once()
        sql_call = mock_cursor.execute.call_args[0][0]
        assert "CREATE TABLE IF NOT EXISTS products" in sql_call
        assert "CREATE INDEX IF NOT EXISTS idx_products_name" in sql_call

    @patch("src.infrastructure.services.DatabaseService.psycopg")
    def test_execute_query(self, mock_psycopg):
        """Test query execution."""
        # Mock connection and cursor
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{"id": "1", "name": "Test"}]
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_psycopg.connect.return_value = mock_connection

        # Execute
        results = self.db_service.execute_query(
            "SELECT * FROM products WHERE id = %(id)s", {"id": "test-id"}
        )

        # Verify
        assert results == [{"id": "1", "name": "Test"}]
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM products WHERE id = %(id)s", {"id": "test-id"}
        )

    @patch("src.infrastructure.services.DatabaseService.psycopg")
    def test_execute_command(self, mock_psycopg):
        """Test command execution."""
        # Mock connection and cursor
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connection.transaction.return_value.__enter__.return_value = (
            mock_connection
        )
        mock_psycopg.connect.return_value = mock_connection

        # Execute
        affected_rows = self.db_service.execute_command(
            "INSERT INTO products (id, name) VALUES (%(id)s, %(name)s)",
            {"id": "test-id", "name": "Test Product"},
        )

        # Verify
        assert affected_rows == 1
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO products (id, name) VALUES (%(id)s, %(name)s)",
            {"id": "test-id", "name": "Test Product"},
        )
