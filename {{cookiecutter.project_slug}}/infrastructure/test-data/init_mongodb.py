{%- if cookiecutter.database_backend == 'mongodb' -%}
#!/usr/bin/env python3
"""
MongoDB test database initialization script.
"""

import os
import sys
from pymongo import MongoClient


def initialize_test_database():
    """Initialize MongoDB test database with sample data."""
    # Connection configuration
    mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    database_name = "{{ cookiecutter.package_name }}_test"
    
    try:
        # Connect to MongoDB
        client = MongoClient(mongodb_uri)
        db = client[database_name]
        
        # Test connection
        client.admin.command('ping')
        print(f"✅ Connected to MongoDB at {mongodb_uri}")
        
        # Initialize test collections with sample data
        collections_data = {
            "test_users": [
                {"_id": "user1", "name": "Alice Johnson", "age": 30, "active": True, "email": "alice@example.com"},
                {"_id": "user2", "name": "Bob Smith", "age": 25, "active": True, "email": "bob@example.com"},
                {"_id": "user3", "name": "Charlie Brown", "age": 35, "active": False, "email": "charlie@example.com"},
                {"_id": "user4", "name": "Diana Prince", "age": 28, "active": True, "email": "diana@example.com"},
                {"_id": "user5", "name": "Eve Wilson", "age": 22, "active": False, "email": "eve@example.com"}
            ],
            "test_orders": [
                {"_id": "order1", "user_id": "user1", "total": 100.50, "status": "completed", "items": 3},
                {"_id": "order2", "user_id": "user2", "total": 75.25, "status": "pending", "items": 2},
                {"_id": "order3", "user_id": "user1", "total": 200.00, "status": "completed", "items": 5},
                {"_id": "order4", "user_id": "user3", "total": 50.75, "status": "cancelled", "items": 1},
                {"_id": "order5", "user_id": "user4", "total": 150.00, "status": "completed", "items": 4}
            ],
            "test_products": [
                {"_id": "prod1", "name": "Widget A", "price": 19.99, "category": "widgets", "in_stock": True},
                {"_id": "prod2", "name": "Gadget B", "price": 29.99, "category": "gadgets", "in_stock": True},
                {"_id": "prod3", "name": "Tool C", "price": 39.99, "category": "tools", "in_stock": False},
                {"_id": "prod4", "name": "Device D", "price": 49.99, "category": "devices", "in_stock": True},
                {"_id": "prod5", "name": "Component E", "price": 9.99, "category": "components", "in_stock": True}
            ]
        }
        
        # Insert data into collections
        for collection_name, documents in collections_data.items():
            collection = db[collection_name]
            
            # Clear existing data
            collection.drop()
            
            # Insert new data
            if documents:
                collection.insert_many(documents)
                print(f"✅ Initialized {collection_name} with {len(documents)} documents")
            else:
                print(f"⚠️ No data to insert for {collection_name}")
        
        # Create indexes for better performance
        db.test_users.create_index("email", unique=True)
        db.test_users.create_index("active")
        db.test_orders.create_index("user_id")
        db.test_orders.create_index("status")
        db.test_products.create_index("category")
        db.test_products.create_index("in_stock")
        
        print("✅ Created indexes for test collections")
        
        # Verify data insertion
        for collection_name in collections_data.keys():
            count = db[collection_name].count_documents({})
            print(f"📊 {collection_name}: {count} documents")
        
        print(f"🎉 MongoDB test database '{database_name}' initialized successfully!")
        
    except Exception as e:
        print(f"❌ Failed to initialize MongoDB test database: {e}")
        sys.exit(1)
    finally:
        if 'client' in locals():
            client.close()


if __name__ == "__main__":
    initialize_test_database()
{%- endif -%}