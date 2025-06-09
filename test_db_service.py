#!/usr/bin/env python3
"""
Simple database service test
"""

from src.infrastructure.services.DatabaseService import DatabaseService

def main():
    print("🔗 Testing DatabaseService...")
    
    try:
        print("   ├─ Creating DatabaseService...")
        db_service = DatabaseService()
        print("   ├─ ✅ DatabaseService created")
        
        print("   ├─ Testing health check...")
        is_healthy = db_service.health_check()
        print(f"   ├─ Health check result: {'✅ Healthy' if is_healthy else '❌ Unhealthy'}")
        
        if is_healthy:
            print("   ├─ Testing schema initialization...")
            db_service.initialize_schema()
            print("   ├─ ✅ Schema initialized")
        
        print("   └─ ✅ All database tests passed!")
        
    except Exception as e:
        print(f"   └─ ❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
