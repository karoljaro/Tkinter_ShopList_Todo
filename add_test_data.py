#!/usr/bin/env python3
"""
Simple script to add more diverse test data to PostgreSQL.
"""

from src.infrastructure.database.PostgreSQLProductRepository import PostgreSQLProductRepository
from src.domain.Product_Entity import _Product

def add_diverse_test_data():
    """Add more diverse test data to see in pgAdmin."""
    print("🛒 Adding diverse shop list data...")
    
    repo = PostgreSQLProductRepository()
    
    diverse_products = [
        # Warzywa i owoce
        _Product(id="fruit-001", name="Banany", quantity=6, purchased=False),
        _Product(id="fruit-002", name="Jabłka Gala", quantity=4, purchased=True),
        _Product(id="veg-001", name="Marchewka", quantity=1, purchased=False),
        _Product(id="veg-002", name="Ziemniaki", quantity=2, purchased=True),
        
        # Nabiał
        _Product(id="dairy-001", name="Jogurt naturalny", quantity=3, purchased=False),
        _Product(id="dairy-002", name="Ser żółty", quantity=1, purchased=False),
        
        # Mięso
        _Product(id="meat-001", name="Kurczak filety", quantity=1, purchased=True),
        _Product(id="meat-002", name="Kiełbasa śląska", quantity=2, purchased=False),
        
        # Napoje
        _Product(id="drink-001", name="Woda mineralna", quantity=6, purchased=False),
        _Product(id="drink-002", name="Sok pomarańczowy", quantity=1, purchased=True),
    ]
    
    added = 0
    for product in diverse_products:
        try:
            # Remove if exists
            existing = repo.get_product_by_id(product.id)
            if existing:
                repo.remove_product(product.id)
            
            repo.add_product(product)
            status = "✅" if product.purchased else "🛒"
            print(f"   {status} {product.name} (qty: {product.quantity})")
            added += 1
        except Exception as e:
            print(f"   ❌ Failed to add {product.name}: {e}")
    
    print(f"\n📊 Added {added} diverse products!")
    print("🌐 Refresh pgAdmin to see all the new data!")
    
    all_products = repo.get_all_products()
    by_category = {}
    for product in all_products:
        category = product.id.split('-')[0] if '-' in product.id else 'other'
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(product)
    
    print(f"\n📈 Database summary ({len(all_products)} total products):")
    for category, products in by_category.items():
        print(f"   {category.title()}: {len(products)} products")

if __name__ == "__main__":
    add_diverse_test_data()
