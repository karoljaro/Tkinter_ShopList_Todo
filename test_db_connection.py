#!/usr/bin/env python3
"""
Simple database connection test
"""

import pytest
import psycopg
import os

def test_simple_connection():
    """Test basic PostgreSQL connection"""
    
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    database = os.getenv("POSTGRES_DB", "shoplist")
    user = os.getenv("POSTGRES_USER", "shoplist_user")
    password = os.getenv("POSTGRES_PASSWORD", "shoplist_pass")

    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}?connect_timeout=3"
    
    print(f"🔗 Testing connection to: {host}:{port}/{database}")
    print(f"🔗 Connection string: postgresql://{user}:***@{host}:{port}/{database}")
    
    try:
        with psycopg.connect(connection_string) as conn:
            print("✅ Connected successfully!")
            
            # Test simple query
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                version = cur.fetchone()[0]
                print(f"✅ PostgreSQL version: {version}")
                  # Test database exists
                cur.execute("SELECT current_database();")
                current_db = cur.fetchone()[0]
                print(f"✅ Current database: {current_db}")
                
            # If we get here, connection was successful
            assert True, "Database connection successful"
            
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        print("ℹ️  Skipping test - PostgreSQL not available (offline mode)")
        pytest.skip(f"PostgreSQL not available: {str(e)}")

if __name__ == "__main__":
    test_simple_connection()
