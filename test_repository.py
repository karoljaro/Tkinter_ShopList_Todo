#!/usr/bin/env python3
"""
Simple repository test
"""

from src.presentation.factories.RepositoryFactory import (
    RepositoryFactory,
    RepositoryType,
)
from src.domain.Product_Entity import _Product as Product


def main():
    print("🗃️  Testing PostgreSQL Repository...")

    try:
        # Test repository creation
        print("   ├─ Creating PostgreSQL repository...")
        repo = RepositoryFactory.create_repository(RepositoryType.POSTGRESQL)
        print("   ├─ ✅ Repository created successfully")

        # Test basic operations
        print("   ├─ Testing basic operations...")

        # Get all products (should work even if empty)
        print("   ├─ Getting all products...")
        all_products = repo.get_all_products()
        print(f"   ├─ ✅ Found {len(all_products)} products")

        # Create a test product
        print("   ├─ Creating test product...")
        test_product = Product(name="Test Product", quantity=5)
        print(f"   ├─ ✅ Test product created: {test_product.name}")

        # Add product
        print("   ├─ Adding product to repository...")
        added_product = repo.add_product(test_product)
        print(f"   ├─ ✅ Product added with ID: {added_product.id}")

        # Get product by ID
        print("   ├─ Retrieving product by ID...")
        retrieved_product = repo.get_product_by_id(added_product.id)
        if retrieved_product:
            print(f"   ├─ ✅ Retrieved product: {retrieved_product.name}")
        else:
            print("   ├─ ❌ Failed to retrieve product by ID")
            return False

        # Update product
        print("   ├─ Updating product...")
        retrieved_product.quantity = 10
        updated_product = repo.update_product(retrieved_product)
        if updated_product and updated_product.quantity == 10:
            print(
                f"   ├─ ✅ Product updated (new quantity: {updated_product.quantity})"
            )
        else:
            print("   ├─ ❌ Failed to update product")
            return False

        # Delete product
        print("   ├─ Deleting product...")
        repo.remove_product(added_product.id)
        deleted_check = repo.get_product_by_id(added_product.id)
        if deleted_check is None:
            print("   ├─ ✅ Product deleted successfully")
        else:
            print("   ├─ ❌ Failed to delete product")
            return False

        print("   └─ ✅ All repository tests passed!")
        return True

    except Exception as e:
        print(f"   └─ ❌ Repository test failed: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 PostgreSQL Repository Integration: ✅ SUCCESS")
    else:
        print("\n❌ PostgreSQL Repository Integration: ❌ FAILED")
