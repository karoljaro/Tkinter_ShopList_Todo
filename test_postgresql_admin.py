#!/usr/bin/env python3
"""
Test script to verify PostgreSQL data persistence and demonstrate CRUD operations.
Run this script to add test data to PostgreSQL and verify it's working.
"""

import time
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
            
            # Verify update
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
        
        return True
        
    except Exception as e:
        print(f"\n❌ PostgreSQL test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def cleanup_test_data():
    """Clean up test data from database."""
    print("\n🧹 Cleaning up test data...")
    try:
        repo = PostgreSQLProductRepository()
        all_products = repo.get_all_products()
        test_products = [p for p in all_products if p.id.startswith("test-")]
        
        for product in test_products:
            repo.remove_product(product.id)
            print(f"   🗑️  Removed: {product.name}")
        
        print(f"✅ Cleaned up {len(test_products)} test products")
        
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")

if __name__ == "__main__":
    print("PostgreSQL Data Persistence Test")
    print("Choose an option:")
    print("1. Test data persistence (add test data)")
    print("2. Clean up test data")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        test_postgresql_data_persistence()
    elif choice == "2":
        cleanup_test_data()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")
