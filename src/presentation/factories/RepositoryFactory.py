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


def load_env_file():
    """Load environment variables from .env file if it exists."""
    env_path = os.path.join(os.path.dirname(__file__), "../../../.env")
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()


load_env_file()


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
        """
        print("🗄️  Attempting to connect to PostgreSQL...")
        try:
            import psycopg
            from psycopg.rows import dict_row
            
            # 3-second timeout
            test_connection_string = "postgresql://shoplist_user:shoplist_pass@localhost:5432/shoplist?connect_timeout=3"
            
            with psycopg.connect(test_connection_string, row_factory=dict_row) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    cursor.fetchone()
            
            # If we got here, PostgreSQL is available
            repo = RepositoryFactory.create_repository(RepositoryType.POSTGRESQL)
            print("✅ Connected to PostgreSQL successfully!")
            return repo
                
        except Exception as e:
            print(f"❌ PostgreSQL unavailable: {type(e).__name__}")
            print("🔄 Falling back to JSON repository...")

        # Try JSON repository
        try:
            repo = RepositoryFactory.create_repository(RepositoryType.JSON)
            print("✅ Using JSON file repository")
            return repo
        except Exception as e:
            print(f"❌ JSON repository failed: {e}")
            print("🔄 Falling back to in-memory repository...")

        # Final fallback to in-memory
        repo = RepositoryFactory.create_repository(RepositoryType.IN_MEMORY)
        print("✅ Using in-memory repository")
        return repo

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

            if hasattr(repo, "health_check"):
                return repo.health_check()

            repo.get_all_products()
            return True

        except Exception:
            return False    
    
    @staticmethod
    def get_default_repository() -> IProductRepository:
        """
        Get the default repository based on environment configuration.
        Uses fallback strategy if primary repository is unavailable.

        :return: Default repository instance
        """
        return RepositoryFactory.create_repository_with_fallback()

    @staticmethod
    def is_postgresql_available() -> bool:
        """
        Check if PostgreSQL repository is available and healthy.

        :return: True if PostgreSQL is available, False otherwise
        """
        return RepositoryFactory.test_repository_connection(RepositoryType.POSTGRESQL)
