import os
from contextlib import contextmanager
from typing import Optional, Iterator, Dict, Any, List
import psycopg
from psycopg import Connection
from psycopg.rows import dict_row


class DatabaseService:
    """
    Infrastructure service for PostgreSQL database operations.
    Manages connections, transactions, and database schema.
    """

    def __init__(self):
        self._connection_string = self._build_connection_string()

    def _build_connection_string(self) -> str:
        """Build PostgreSQL connection string from environment variables."""
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")
        database = os.getenv("POSTGRES_DB", "shoplist")
        user = os.getenv("POSTGRES_USER", "shoplist_user")
        password = os.getenv("POSTGRES_PASSWORD", "shoplist_pass")

        return f"postgresql://{user}:{password}@{host}:{port}/{database}"

    @contextmanager
    def get_connection(self) -> Iterator[Connection[Dict[str, Any]]]:
        """
        Get database connection with automatic cleanup.

        :yield: Database connection
        """
        connection = None
        try:
            connection = psycopg.connect(self._connection_string, row_factory=dict_row)
            yield connection
        finally:
            if connection:
                connection.close()

    @contextmanager
    def get_transaction(self) -> Iterator[Connection[Dict[str, Any]]]:
        """
        Get database connection with transaction management.

        :yield: Database connection with transaction
        """
        with self.get_connection() as conn:
            try:
                with conn.transaction():
                    yield conn
            except Exception:
                # Transaction is automatically rolled back
                raise

    def health_check(self) -> bool:
        """
        Check if database connection is healthy.

        :return: True if database is accessible
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    return cursor.fetchone() is not None
        except Exception:
            return False

    def initialize_schema(self) -> None:
        """
        Initialize database schema for products.
        Creates tables if they don't exist.
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS products (
            id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            quantity INTEGER NOT NULL CHECK (quantity > 0),
            purchased BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_products_name ON products(name);
        CREATE INDEX IF NOT EXISTS idx_products_purchased ON products(purchased);
        """

        with self.get_transaction() as conn:
            with conn.cursor() as cursor:
                cursor.execute(create_table_sql)

    def execute_query(
        self, query: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute SELECT query and return results.

        :param query: SQL query
        :param params: Query parameters
        :return: List of rows as dictionaries
        """
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params or {})
                return cursor.fetchall()

    def execute_command(
        self, command: str, params: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Execute INSERT/UPDATE/DELETE command.

        :param command: SQL command
        :param params: Command parameters
        :return: Number of affected rows
        """
        with self.get_transaction() as conn:
            with conn.cursor() as cursor:
                cursor.execute(command, params or {})
                return cursor.rowcount
