import pytest
import os
from unittest.mock import Mock, patch, call
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
        config = {"file_path": "custom/path/products.json"}
        repository = RepositoryFactory.create_repository(RepositoryType.JSON, config)

        assert isinstance(repository, JsonProductRepository)

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

        repository = RepositoryFactory.create_repository()

        # Should create JSON repository as default
        assert isinstance(repository, JsonProductRepository)

    def test_create_repository_with_fallback_postgresql_success(self):
        """Test fallback strategy when PostgreSQL is available."""
        # Mock PostgreSQL repository that works
        mock_postgresql_repo = Mock(spec=IProductRepository)
        mock_postgresql_repo.get_all_products.return_value = []

        with patch.object(RepositoryFactory, "create_repository") as mock_create:
            mock_create.return_value = mock_postgresql_repo

            repository = RepositoryFactory.create_repository_with_fallback()
            assert repository == mock_postgresql_repo
            mock_create.assert_called_once_with(RepositoryType.POSTGRESQL)

    def test_create_repository_with_fallback_postgresql_fails_json_success(self):
        """Test fallback strategy when PostgreSQL fails but JSON works."""
        # Mock PostgreSQL repository that fails
        mock_postgresql_repo = Mock(spec=IProductRepository)
        mock_postgresql_repo.get_all_products.side_effect = Exception(
            "DB connection failed"
        )

        # Mock JSON repository that works
        mock_json_repo = Mock(spec=IProductRepository)
        mock_json_repo.get_all_products.return_value = []

        with patch.object(RepositoryFactory, "create_repository") as mock_create:
            mock_create.side_effect = [mock_postgresql_repo, mock_json_repo]

            repository = RepositoryFactory.create_repository_with_fallback()

            assert repository == mock_json_repo
            assert mock_create.call_count == 2

    def test_create_repository_with_fallback_all_fail_returns_memory(self):
        """Test fallback strategy when all external repositories fail."""
        with patch.object(RepositoryFactory, "create_repository") as mock_create:
            # Mock PostgreSQL repository that fails health check
            mock_postgresql_repo = Mock(spec=IProductRepository)
            mock_postgresql_repo.get_all_products.side_effect = Exception(
                "DB connection failed"
            )

            # Mock in-memory repository that always works
            mock_memory_repo = Mock(spec=IProductRepository)
            mock_memory_repo.get_all_products.return_value = []

            # Set up side effects for create_repository calls
            # PostgreSQL creation succeeds but health check fails
            # JSON creation fails entirely
            # In-memory creation succeeds
            mock_create.side_effect = [
                mock_postgresql_repo,  # First call for PostgreSQL
                Exception("JSON file not accessible"),  # Second call for JSON fails
                mock_memory_repo,  # Third call for in-memory
            ]

            repository = RepositoryFactory.create_repository_with_fallback()

            # Verify that create_repository was called 3 times
            assert mock_create.call_count == 3

            # Verify the call sequence
            expected_calls = [
                call(RepositoryType.POSTGRESQL),
                call(RepositoryType.JSON),
                call(RepositoryType.IN_MEMORY),
            ]
            mock_create.assert_has_calls(expected_calls)

            # Verify the PostgreSQL repo was tested and failed
            mock_postgresql_repo.get_all_products.assert_called_once()

            # Verify that the final repository behaves as expected (in-memory)
            assert repository.get_all_products() == []

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
