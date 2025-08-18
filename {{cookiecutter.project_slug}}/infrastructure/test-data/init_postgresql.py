{%- if cookiecutter.database_backend == 'postgresql' -%}
#!/usr/bin/env python3
"""
PostgreSQL test database initialization script.
"""

import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor


def initialize_test_database():
    """Initialize PostgreSQL test database with sample data."""
    # Connection configuration
    database_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/{{ cookiecutter.package_name }}_test")
    
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(database_url)
        conn.autocommit = True
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        print(f"✅ Connected to PostgreSQL at {database_url}")
        
        # Create test tables
        tables = {
            "test_users": """
                CREATE TABLE IF NOT EXISTS test_users (
                    id VARCHAR(50) PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    age INTEGER,
                    active BOOLEAN DEFAULT TRUE,
                    email VARCHAR(150) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            "test_orders": """
                CREATE TABLE IF NOT EXISTS test_orders (
                    id VARCHAR(50) PRIMARY KEY,
                    user_id VARCHAR(50) REFERENCES test_users(id),
                    total DECIMAL(10,2) NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    items INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            "test_products": """
                CREATE TABLE IF NOT EXISTS test_products (
                    id VARCHAR(50) PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    category VARCHAR(50),
                    in_stock BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
        }
        
        # Create tables
        for table_name, create_sql in tables.items():
            cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE")
            cursor.execute(create_sql)
            print(f"✅ Created table {table_name}")
        
        # Insert sample data
        sample_data = {
            "test_users": [
                ("user1", "Alice Johnson", 30, True, "alice@example.com"),
                ("user2", "Bob Smith", 25, True, "bob@example.com"),
                ("user3", "Charlie Brown", 35, False, "charlie@example.com"),
                ("user4", "Diana Prince", 28, True, "diana@example.com"),
                ("user5", "Eve Wilson", 22, False, "eve@example.com")
            ],
            "test_orders": [
                ("order1", "user1", 100.50, "completed", 3),
                ("order2", "user2", 75.25, "pending", 2),
                ("order3", "user1", 200.00, "completed", 5),
                ("order4", "user3", 50.75, "cancelled", 1),
                ("order5", "user4", 150.00, "completed", 4)
            ],
            "test_products": [
                ("prod1", "Widget A", 19.99, "widgets", True),
                ("prod2", "Gadget B", 29.99, "gadgets", True),
                ("prod3", "Tool C", 39.99, "tools", False),
                ("prod4", "Device D", 49.99, "devices", True),
                ("prod5", "Component E", 9.99, "components", True)
            ]
        }
        
        # Insert data
        for table_name, records in sample_data.items():
            if table_name == "test_users":
                insert_sql = """
                    INSERT INTO test_users (id, name, age, active, email) 
                    VALUES (%s, %s, %s, %s, %s)
                """
            elif table_name == "test_orders":
                insert_sql = """
                    INSERT INTO test_orders (id, user_id, total, status, items) 
                    VALUES (%s, %s, %s, %s, %s)
                """
            elif table_name == "test_products":
                insert_sql = """
                    INSERT INTO test_products (id, name, price, category, in_stock) 
                    VALUES (%s, %s, %s, %s, %s)
                """
            
            cursor.executemany(insert_sql, records)
            print(f"✅ Inserted {len(records)} records into {table_name}")
        
        # Create indexes for better performance
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_users_email ON test_users(email)",
            "CREATE INDEX IF NOT EXISTS idx_users_active ON test_users(active)",
            "CREATE INDEX IF NOT EXISTS idx_orders_user_id ON test_orders(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_orders_status ON test_orders(status)",
            "CREATE INDEX IF NOT EXISTS idx_products_category ON test_products(category)",
            "CREATE INDEX IF NOT EXISTS idx_products_in_stock ON test_products(in_stock)"
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)
        
        print("✅ Created indexes for test tables")
        
        # Verify data insertion
        for table_name in sample_data.keys():
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"📊 {table_name}: {count} records")
        
        print(f"🎉 PostgreSQL test database initialized successfully!")
        
    except Exception as e:
        print(f"❌ Failed to initialize PostgreSQL test database: {e}")
        sys.exit(1)
    finally:
        if 'conn' in locals():
            conn.close()


if __name__ == "__main__":
    initialize_test_database()
{%- endif -%}