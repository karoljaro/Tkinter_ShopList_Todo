import os
from enum import Enum
from typing import Optional
from src.application.repositories.IProductRepository import IProductRepository
from src.infrastructure.InMemoryProductRepository import InMemoryProductRepository
from src.infrastructure.JsonProductRepository import JsonProductRepository
from src.infrastructure.database.PostgreSQLProductRepository import (
    PostgreSQLProductRepository,
)
from src.infrastructure.services.DatabaseService import DatabaseService


class RepositoryType(Enum):
    """Enumeration of available repository types."""

    IN_MEMORY = "in_memory"
    JSON = "json"
    POSTGRESQL = "postgresql"


class RepositoryFactory:
    """
    Presentation layer factory for creating repository instances.
    Implements Factory pattern with environment-based configuration.
    """

    @staticmethod
    def create_repository(
        repository_type: Optional[RepositoryType] = None, config: Optional[dict] = None
    ) -> IProductRepository:
        """
        Create a repository instance based on type and configuration.

        :param repository_type: Type of repository to create (defaults to env config)
        :param config: Optional configuration dictionary
        :return: Repository instance implementing IProductRepository
        """
        if repository_type is None:
            repository_type = RepositoryFactory._get_default_repository_type()

        config = config or {}

        if repository_type == RepositoryType.IN_MEMORY:
            return RepositoryFactory._create_in_memory_repository()

        elif repository_type == RepositoryType.JSON:
            return RepositoryFactory._create_json_repository(config)

        elif repository_type == RepositoryType.POSTGRESQL:
            return RepositoryFactory._create_postgresql_repository(config)

        else:
            raise ValueError(f"Unknown repository type: {repository_type}")

    @staticmethod
    def _get_default_repository_type() -> RepositoryType:
        """Get default repository type from environment variables."""
        repo_type = os.getenv("REPOSITORY_TYPE", "json").lower()

        try:
            return RepositoryType(repo_type)
        except ValueError:
            # Fallback to JSON if invalid type specified
            return RepositoryType.JSON

    @staticmethod
    def _create_in_memory_repository() -> InMemoryProductRepository:
        """Create in-memory repository instance."""
        return InMemoryProductRepository()

    @staticmethod
    def _create_json_repository(config: dict) -> JsonProductRepository:
        """Create JSON file repository instance."""
        default_path = os.path.join("src", "infrastructure", "data", "products.json")
        file_path = config.get("file_path", os.getenv("JSON_FILE_PATH", default_path))

        return JsonProductRepository(file_path)

    @staticmethod
    def _create_postgresql_repository(config: dict) -> PostgreSQLProductRepository:
        """Create PostgreSQL repository instance."""
        database_service = config.get("database_service")

        if database_service is None:
            database_service = DatabaseService()

        return PostgreSQLProductRepository(database_service)

    @staticmethod
    def create_repository_with_fallback() -> IProductRepository:
        """
        Create repository with automatic fallback strategy.
        Tries PostgreSQL first, then JSON, finally in-memory.

        :return: Working repository instance
        """  # Try PostgreSQL first
        try:
            repo = RepositoryFactory.create_repository(RepositoryType.POSTGRESQL)
            # Test repository availability by trying to get all products
            repo.get_all_products()
            return repo
        except Exception:
            pass  # Fall back to next option

        # Try JSON repository
        try:
            return RepositoryFactory.create_repository(RepositoryType.JSON)
        except Exception:
            pass  # Fall back to in-memory

        # Final fallback to in-memory
        return RepositoryFactory.create_repository(RepositoryType.IN_MEMORY)

    @staticmethod
    def get_available_repository_types() -> list[RepositoryType]:
        """
        Get list of available repository types.

        :return: List of available repository types
        """
        return list(RepositoryType)

    @staticmethod
    def test_repository_connection(repository_type: RepositoryType) -> bool:
        """
        Test if a specific repository type can be connected to.

        :param repository_type: Repository type to test
        :return: True if connection successful
        """
        try:
            repo = RepositoryFactory.create_repository(repository_type)

            # For PostgreSQL, check health
            if hasattr(repo, "health_check"):
                return repo.health_check()

            # For other types, try a simple operation
            repo.get_all_products()
            return True

        except Exception:
            return False
