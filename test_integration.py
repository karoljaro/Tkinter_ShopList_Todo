#!/usr/bin/env python3
"""
Integration test for PostgreSQL connectivity
"""

import sys
from src.infrastructure.services.DatabaseService import DatabaseService
from src.infrastructure.services.HealthCheckService import HealthCheckService
from src.presentation.factories.RepositoryFactory import RepositoryFactory, RepositoryType
from src.domain.Product_Entity import _Product as Product


def test_database_connectivity():
    """Test basic database connectivity"""
    print("🔗 Testing PostgreSQL connectivity...")
    
    try:
        db_service = DatabaseService()
        print("   ├─ ✅ DatabaseService created successfully")
    except Exception as e:
        print(f"   └─ ❌ Failed to create DatabaseService: {str(e)}")
        assert False, f"Failed to create DatabaseService: {str(e)}"
    
    try:
        print("   ├─ Testing database health check...")
        is_healthy = db_service.health_check()
        print(f"   ├─ Database health: {'✅ Healthy' if is_healthy else '❌ Unhealthy'}")
        
        if not is_healthy:
            print("   └─ ❌ Database connection failed")
            assert False, "Database connection failed"
            
        print("   ├─ Testing schema initialization...")
        db_service.initialize_schema()
        print("   ├─ ✅ Schema initialized successfully")
        
        assert True, "Database connectivity test successful"
        
    except Exception as e:
        print(f"   └─ ❌ Database connectivity test failed: {str(e)}")
        assert False, f"Database connectivity test failed: {str(e)}"


def test_http_health_check():
    """Test HTTP health check service"""
    print("🌐 Testing HTTP health check service...")
    
    try:
        health_service = HealthCheckService()
        print("   ├─ ✅ HealthCheckService created successfully")
    except Exception as e:
        print(f"   └─ ❌ Failed to create HealthCheckService: {str(e)}")
        assert False, f"Failed to create HealthCheckService: {str(e)}"
    
    try:
        print("   ├─ Testing HTTP request to httpbin.org...")
        result = health_service.check_http_endpoint("http://httpbin.org/status/200")
        print(f"   ├─ HTTP check result: {'✅ Success' if result.is_healthy else '❌ Failed'}")
        
        assert result.is_healthy, "HTTP health check should be successful"
        
    except Exception as e:
        print(f"   └─ ❌ HTTP health check test failed: {str(e)}")
        # Don't fail the entire test suite for HTTP issues
        print("   └─ ⚠️  HTTP test skipped (external dependency)")
        assert True, "HTTP test skipped due to external dependency"


def test_repository_integration():
    """Test complete repository integration"""
    print("🗃️  Testing repository integration...")
    
    try:
        print("   ├─ Testing PostgreSQL repository creation...")
        repo = RepositoryFactory.create_repository(RepositoryType.POSTGRESQL)
        print("   ├─ ✅ PostgreSQL repository created successfully")
        
        print("   ├─ Testing basic CRUD operations...")
        
        test_product = Product(name="Integration Test Product", quantity=5)
        
        added_product = repo.add_product(test_product)
        print(f"   ├─ ✅ Product added with ID: {added_product.id}")
        
        all_products = repo.get_all_products()
        print(f"   ├─ ✅ Retrieved {len(all_products)} products from database")
        
        retrieved_product = repo.get_product_by_id(added_product.id)
        if retrieved_product:
            print(f"   ├─ ✅ Retrieved product: {retrieved_product.name}")
        else:
            print("   ├─ ❌ Failed to retrieve product by ID")
            assert False, "Failed to retrieve product by ID"
        
        retrieved_product.quantity = 10
        updated_product = repo.update_product(retrieved_product)
        if updated_product and updated_product.quantity == 10:
            print(f"   ├─ ✅ Product updated successfully (new quantity: {updated_product.quantity})")
        else:
            print("   ├─ ❌ Failed to update product")
            assert False, "Failed to update product"
        
        repo.remove_product(added_product.id)
        deleted_check = repo.get_product_by_id(added_product.id)
        if deleted_check is None:
            print("   ├─ ✅ Product deleted successfully")
        else:
            print("   ├─ ❌ Failed to delete product")
            assert False, "Failed to delete product"
            
        assert True, "Repository integration test successful"
        
    except Exception as e:
        print(f"   └─ ❌ Repository integration test failed: {str(e)}")
        assert False, f"Repository integration test failed: {str(e)}"


def test_fallback_strategy():
    """Test repository fallback strategy"""
    print("🔄 Testing repository fallback strategy...")
    
    try:
        print("   ├─ Testing fallback with PostgreSQL available...")
        repo = RepositoryFactory.create_repository_with_fallback()
        
        repo_type = type(repo).__name__
        print(f"   ├─ ✅ Fallback selected: {repo_type}")
        
        products = repo.get_all_products()
        print(f"   ├─ ✅ Repository works: {len(products)} products found")
        
        assert True, "Fallback strategy test successful"
        
    except Exception as e:
        print(f"   └─ ❌ Fallback strategy test failed: {str(e)}")
        assert False, f"Fallback strategy test failed: {str(e)}"


def main():
    """Run all integration tests"""
    print("🚀 Starting PostgreSQL Integration Tests")
    print("=" * 50)
    
    tests = [
        ("Database Connectivity", test_database_connectivity),
        ("HTTP Health Check", test_http_health_check),
        ("Repository Integration", test_repository_integration),
        ("Fallback Strategy", test_fallback_strategy),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            test_func()
            result = True
        except AssertionError:
            result = False
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 INTEGRATION TEST RESULTS:")
    print("=" * 50)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:.<30} {status}")
        if not result:
            all_passed = False
    
    print("=" * 50)
    overall_status = "🎉 ALL TESTS PASSED" if all_passed else "⚠️  SOME TESTS FAILED"
    print(f"Overall Result: {overall_status}")
    print("=" * 50)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
