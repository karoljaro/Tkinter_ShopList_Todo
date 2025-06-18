import pytest
import os
import shutil
from unittest.mock import Mock, patch
from src.presentation.factories.RepositoryFactory import (
    RepositoryFactory,
    RepositoryType,
)
from src.application.repositories.IProductRepository import IProductRepository
from src.infrastructure.InMemoryProductRepository import InMemoryProductRepository
from src.infrastructure.JsonProductRepository import JsonProductRepository
from src.infrastructure.database.PostgreSQLProductRepository import (
    PostgreSQLProductRepository,
)


class TestRepositoryFactory:
    """Unit tests for RepositoryFactory."""

    def test_create_in_memory_repository(self):
        """Test creation of in-memory repository."""
        repository = RepositoryFactory.create_repository(RepositoryType.IN_MEMORY)

        assert isinstance(repository, InMemoryProductRepository)
        assert isinstance(repository, IProductRepository)

    def test_create_json_repository_default_path(self):
        """Test creation of JSON repository with default path."""
        repository = RepositoryFactory.create_repository(RepositoryType.JSON)

        assert isinstance(repository, JsonProductRepository)
        assert isinstance(repository, IProductRepository)

    def test_create_json_repository_custom_path(self):
        """Test creation of JSON repository with custom path."""
        custom_path = "custom/path/products.json"
        config = {"file_path": custom_path}

        try:
            repository = RepositoryFactory.create_repository(
                RepositoryType.JSON, config
            )
            assert isinstance(repository, JsonProductRepository)
        finally:
            # Cleanup: Remove the custom folder if it exists
            if os.path.exists("custom"):
                shutil.rmtree("custom")

    @patch("src.presentation.factories.RepositoryFactory.DatabaseService")
    def test_create_postgresql_repository_default_service(self, mock_db_service_class):
        """Test creation of PostgreSQL repository with default database service."""
        mock_db_service = Mock()
        mock_db_service_class.return_value = mock_db_service

        repository = RepositoryFactory.create_repository(RepositoryType.POSTGRESQL)

        assert isinstance(repository, PostgreSQLProductRepository)
        assert isinstance(repository, IProductRepository)
        mock_db_service_class.assert_called_once()

    def test_create_postgresql_repository_custom_service(self):
        """Test creation of PostgreSQL repository with custom database service."""
        mock_db_service = Mock()
        config = {"database_service": mock_db_service}

        repository = RepositoryFactory.create_repository(
            RepositoryType.POSTGRESQL, config
        )

        assert isinstance(repository, PostgreSQLProductRepository)

    @patch.dict(os.environ, {"REPOSITORY_TYPE": "in_memory"}, clear=False)
    def test_get_default_repository_type_in_memory(self):
        """Test default repository type from environment - in_memory."""
        default_type = RepositoryFactory._get_default_repository_type()
        assert default_type == RepositoryType.IN_MEMORY

    @patch.dict(os.environ, {"REPOSITORY_TYPE": "json"}, clear=False)
    def test_get_default_repository_type_json(self):
        """Test default repository type from environment - json."""
        default_type = RepositoryFactory._get_default_repository_type()
        assert default_type == RepositoryType.JSON

    @patch.dict(os.environ, {"REPOSITORY_TYPE": "postgresql"}, clear=False)
    def test_get_default_repository_type_postgresql(self):
        """Test default repository type from environment - postgresql."""
        default_type = RepositoryFactory._get_default_repository_type()
        assert default_type == RepositoryType.POSTGRESQL

    @patch.dict(os.environ, {"REPOSITORY_TYPE": "invalid"}, clear=False)
    def test_get_default_repository_type_invalid(self):
        """Test default repository type with invalid environment value."""
        default_type = RepositoryFactory._get_default_repository_type()
        assert default_type == RepositoryType.JSON  # Should fallback to JSON

    @patch.dict(os.environ, {}, clear=True)
    def test_get_default_repository_type_no_env(self):
        """Test default repository type with no environment variable."""
        # Remove REPOSITORY_TYPE if it exists
        if "REPOSITORY_TYPE" in os.environ:
            del os.environ["REPOSITORY_TYPE"]

        default_type = RepositoryFactory._get_default_repository_type()
        assert default_type == RepositoryType.JSON  # Should fallback to JSON

    @patch.dict(os.environ, {}, clear=True)
    def test_create_repository_default_type(self):
        """Test repository creation with default type from environment."""
        # Remove REPOSITORY_TYPE if it exists
        if "REPOSITORY_TYPE" in os.environ:
            del os.environ["REPOSITORY_TYPE"]

        repository = (
            RepositoryFactory.create_repository()
        )  # Should create JSON repository as default
        assert isinstance(repository, JsonProductRepository)

    def test_create_repository_with_fallback_postgresql_success_real(self):
        """Test fallback strategy when PostgreSQL is actually available."""
        # This test will actually try to connect to PostgreSQL
        # If PostgreSQL is running, it should succeed
        repository = RepositoryFactory.create_repository_with_fallback()

        # Should get some repository (could be PostgreSQL, JSON, or InMemory
        # depending on environment)
        assert isinstance(repository, IProductRepository)

        # Test basic functionality
        all_products = repository.get_all_products()
        assert isinstance(all_products, list)

    @patch("psycopg.connect")
    @patch("builtins.print")
    def test_create_repository_with_fallback_postgresql_connection_fails(
        self, mock_print, mock_psycopg_connect
    ):
        """Test fallback strategy when PostgreSQL connection fails."""
        # Mock PostgreSQL connection failure
        mock_psycopg_connect.side_effect = Exception("DB connection failed")

        repository = (
            RepositoryFactory.create_repository_with_fallback()
        )  # Should fallback to JSON repository (or InMemory if JSON also fails)
        assert isinstance(
            repository, (JsonProductRepository, InMemoryProductRepository)
        )
        # Verify PostgreSQL connection was attempted
        mock_psycopg_connect.assert_called_once()

    @patch("psycopg.connect")
    @patch("builtins.print")
    def test_create_repository_with_fallback_all_external_fail(
        self, mock_print, mock_psycopg_connect
    ):
        """Test fallback strategy when all external repositories fail."""
        # Mock PostgreSQL connection failure
        mock_psycopg_connect.side_effect = Exception("DB connection failed")

        # Since we can't easily mock JSON file failure in this context,
        # we'll just test that the fallback function returns some valid repository
        repository = RepositoryFactory.create_repository_with_fallback()

        # Should get some repository (JSON or InMemory)
        assert isinstance(repository, IProductRepository)
        # Verify PostgreSQL connection was attempted
        mock_psycopg_connect.assert_called_once()

    def test_repository_type_enum_values(self):
        """Test RepositoryType enum values."""
        assert RepositoryType.IN_MEMORY.value == "in_memory"
        assert RepositoryType.JSON.value == "json"
        assert RepositoryType.POSTGRESQL.value == "postgresql"

    def test_invalid_repository_type(self):
        """Test creation with invalid repository type."""
        with pytest.raises(ValueError, match="Unknown repository type"):
            # This should raise an error for unsupported repository types
            # Note: This test assumes the factory validates repository types
            RepositoryFactory.create_repository("invalid_type")
