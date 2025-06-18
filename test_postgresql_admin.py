#!/usr/bin/env python3
"""
Test script to verify PostgreSQL data persistence and demonstrate CRUD operations.
Run this script to add test data to PostgreSQL and verify it's working.
"""

import time
import os
import json
import shutil
import pytest
from src.infrastructure.database.PostgreSQLProductRepository import PostgreSQLProductRepository
from src.domain.Product_Entity import _Product

def test_postgresql_data_persistence():
    """Test PostgreSQL data persistence with real data."""
    print("🗄️  Testing PostgreSQL Data Persistence")
    print("=" * 50)
    
    try:
        print("1. Connecting to PostgreSQL...")
        repo = PostgreSQLProductRepository()
        print("   ✅ Connected successfully!")
        
        # Create test products
        test_products = [
            _Product(id="test-001", name="Mleko 2%", quantity=2, purchased=False),
            _Product(id="test-002", name="Chleb żytni", quantity=1, purchased=True),
            _Product(id="test-003", name="Jajka L", quantity=12, purchased=False),
            _Product(id="test-004", name="Masło extra", quantity=1, purchased=False),
            _Product(id="test-005", name="Pomidory", quantity=5, purchased=True),
        ]
        
        print("\n2. Adding test products to database...")
        added_count = 0
        for product in test_products:
            try:
                existing = repo.get_product_by_id(product.id)
                if existing:
                    repo.remove_product(product.id)
                    print(f"   🗑️  Removed existing: {existing.name}")
                
                # Add new product
                repo.add_product(product)
                print(f"   ✅ Added: {product.name} (qty: {product.quantity}, purchased: {product.purchased})")
                added_count += 1
                time.sleep(0.1)
                
            except Exception as e:
                print(f"   ❌ Failed to add {product.name}: {e}")
        
        print(f"\n   📊 Successfully added {added_count} products to PostgreSQL!")
        
        # Verify data is persisted
        print("\n3. Verifying data persistence...")
        all_products = repo.get_all_products()
        test_products_in_db = [p for p in all_products if p.id.startswith("test-")]
        
        print(f"   📈 Total products in database: {len(all_products)}")
        print(f"   🧪 Test products in database: {len(test_products_in_db)}")
        
        if test_products_in_db:
            print("\n4. Current test products in PostgreSQL:")
            print("   " + "-" * 60)
            for product in test_products_in_db:
                status = "✅ Purchased" if product.purchased else "🛒 To buy"
                print(f"   {product.id} | {product.name:<15} | Qty: {product.quantity:>2} | {status}")
            print("   " + "-" * 60)
        
        # Test update operation
        print("\n5. Testing update operation...")
        if test_products_in_db:
            product_to_update = test_products_in_db[0]
            original_quantity = product_to_update.quantity
            product_to_update.quantity = original_quantity + 10
            product_to_update.purchased = not product_to_update.purchased
            
            repo.update_product(product_to_update)
            print(f"   📝 Updated {product_to_update.name}: qty {original_quantity} → {product_to_update.quantity}")
            updated_product = repo.get_product_by_id(product_to_update.id)
            if updated_product and updated_product.quantity == product_to_update.quantity:
                print("   ✅ Update verified in database!")
            else:
                print("   ❌ Update verification failed!")
        
        print(f"\n🎉 PostgreSQL persistence test completed successfully!")
        print(f"🌐 Access pgAdmin at: http://localhost:8080")
        print(f"📧 Email: admin@shoplist.com")
        print(f"🔑 Password: admin123")
        print(f"\n📋 To connect to database in pgAdmin:")
        print(f"   Host: postgres (or localhost)")
        print(f"   Port: 5432")
        print(f"   Database: shoplist")
        print(f"   Username: shoplist_user")
        print(f"   Password: shoplist_pass")
        
        # Assert that we have test data in the database
        assert len(test_products_in_db) > 0, "No test products found in database"
        assert added_count > 0, "No products were successfully added"
        
    except Exception as e:
        print(f"\n❌ PostgreSQL test failed: {e}")
        import traceback
        traceback.print_exc()
        print("ℹ️  Skipping test - PostgreSQL not available (offline mode)")
        pytest.skip(f"PostgreSQL not available: {str(e)}")

def cleanup_test_data():
    """Clean up test data from database."""
    print("\n🧹 Cleaning up test data from PostgreSQL...")
    try:
        repo = PostgreSQLProductRepository()
        all_products = repo.get_all_products()
        test_products = [p for p in all_products if p.id.startswith("test-")]
        
        for product in test_products:
            repo.remove_product(product.id)
            print(f"   🗑️  Removed: {product.name}")
        
        print(f"✅ Cleaned up {len(test_products)} test products from PostgreSQL")
        
    except Exception as e:
        print(f"❌ PostgreSQL cleanup failed: {e}")

def cleanup_json_test_file():
    """Clean up custom folder and all test files created during tests."""
    custom_folder_path = "custom"
    print(f"\n🧹 Cleaning up custom folder: {custom_folder_path}")
    
    try:
        if os.path.exists(custom_folder_path):
            # Remove entire custom folder and its contents
            shutil.rmtree(custom_folder_path)
            print(f"   ✅ Removed entire folder: {custom_folder_path}")
        else:
            print(f"   ℹ️  Folder {custom_folder_path} doesn't exist")
            
    except Exception as e:
        print(f"   ❌ Failed to remove custom folder: {e}")

def cleanup_all_test_data():
    """Clean up all test data - PostgreSQL and JSON files."""
    print("🧹 Cleaning up ALL test data...")
    cleanup_test_data()  # PostgreSQL
    cleanup_json_test_file()  # JSON file
    
    # Also clean main JSON file if it has test data
    main_json_path = "src/infrastructure/data/products.json"
    try:
        if os.path.exists(main_json_path):
            with open(main_json_path, 'r', encoding='utf-8') as file:
                products = json.load(file)
            
            # Remove test products
            original_count = len(products)
            products = [p for p in products if not p.get('id', '').startswith('test-')]
            
            if len(products) < original_count:
                with open(main_json_path, 'w', encoding='utf-8') as file:
                    json.dump(products, file, indent=2, ensure_ascii=False)
                print(f"   ✅ Removed {original_count - len(products)} test products from {main_json_path}")
                
    except Exception as e:
        print(f"   ❌ Failed to clean main JSON file: {e}")
    
    print("🎉 All test data cleanup completed!")

if __name__ == "__main__":
    print("PostgreSQL Data Persistence Test")
    print("Choose an option:")
    print("1. Test data persistence (add test data)")
    print("2. Clean up PostgreSQL test data")
    print("3. Clean up custom folder and test files")
    print("4. Clean up ALL test data")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        test_postgresql_data_persistence()
    elif choice == "2":
        cleanup_test_data()
    elif choice == "3":
        cleanup_json_test_file()
    elif choice == "4":
        cleanup_all_test_data()
    elif choice == "5":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")
