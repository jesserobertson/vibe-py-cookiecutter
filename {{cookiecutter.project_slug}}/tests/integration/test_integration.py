{%- if cookiecutter.database_backend != "none" -%}
"""
Integration tests for {{ cookiecutter.project_name }}.
These tests require external dependencies like databases.
"""

import pytest
{%- if cookiecutter.use_async == "yes" %}
import asyncio
{%- endif %}

import {{ cookiecutter.package_name }}


@pytest.mark.integration
class TestDatabaseIntegration:
    """Test database integration functionality."""

{%- if cookiecutter.database_backend == "mongodb" %}
    def test_mongodb_connection(self, mongodb_client, test_database_name):
        """Test MongoDB connection and basic operations."""
        db = mongodb_client[test_database_name]
        collection = db.test_collection
        
        # Test insert
        test_doc = {"name": "test", "value": 42}
        result = collection.insert_one(test_doc)
        assert result.inserted_id is not None
        
        # Test find
        found_doc = collection.find_one({"name": "test"})
        assert found_doc is not None
        assert found_doc["value"] == 42
        
        # Test count
        count = collection.count_documents({})
        assert count == 1

    def test_mongodb_operations_with_sample_data(self, test_collection, sample_data):
        """Test MongoDB operations with sample data."""
        # Insert sample data
        test_records = sample_data["test_records"]
        result = test_collection.insert_many(test_records)
        assert len(result.inserted_ids) == len(test_records)
        
        # Test filtering
        active_records = list(test_collection.find({"active": True}))
        assert len(active_records) == 2
        
        # Test update
        test_collection.update_one(
            {"id": 1},
            {"$set": {"name": "Updated Test Item 1"}}
        )
        
        updated_record = test_collection.find_one({"id": 1})
        assert updated_record["name"] == "Updated Test Item 1"

{%- if cookiecutter.use_async == "yes" %}
    @pytest.mark.asyncio
    async def test_async_mongodb_connection(self, async_mongodb_client, test_database_name):
        """Test async MongoDB connection and operations."""
        db = async_mongodb_client[test_database_name]
        collection = db.test_collection_async
        
        # Test async insert
        test_doc = {"name": "async_test", "value": 100}
        result = await collection.insert_one(test_doc)
        assert result.inserted_id is not None
        
        # Test async find
        found_doc = await collection.find_one({"name": "async_test"})
        assert found_doc is not None
        assert found_doc["value"] == 100
        
        # Test async count
        count = await collection.count_documents({})
        assert count == 1
        
        # Clean up
        await collection.delete_many({})

    @pytest.mark.asyncio
    async def test_concurrent_mongodb_operations(self, async_mongodb_client, test_database_name):
        """Test concurrent MongoDB operations."""
        db = async_mongodb_client[test_database_name]
        collection = db.test_collection_concurrent
        
        # Create multiple concurrent insert operations
        async def insert_document(doc_id: int):
            return await collection.insert_one({"id": doc_id, "name": f"doc_{doc_id}"})
        
        # Run concurrent inserts
        tasks = [insert_document(i) for i in range(5)]
        results = await asyncio.gather(*tasks)
        
        # Verify all inserts succeeded
        assert len(results) == 5
        assert all(result.inserted_id is not None for result in results)
        
        # Verify all documents exist
        count = await collection.count_documents({})
        assert count == 5
        
        # Clean up
        await collection.delete_many({})
{%- endif %}

{%- elif cookiecutter.database_backend == "postgresql" %}
    def test_postgresql_connection(self, postgres_connection):
        """Test PostgreSQL connection and basic operations."""
        cursor = postgres_connection.cursor()
        
        # Create test table
        cursor.execute("""
            CREATE TEMPORARY TABLE test_table (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                value INTEGER
            )
        """)
        
        # Test insert
        cursor.execute(
            "INSERT INTO test_table (name, value) VALUES (%s, %s) RETURNING id",
            ("test", 42)
        )
        row_id = cursor.fetchone()[0]
        assert row_id is not None
        
        # Test select
        cursor.execute("SELECT name, value FROM test_table WHERE id = %s", (row_id,))
        row = cursor.fetchone()
        assert row is not None
        assert row[0] == "test"
        assert row[1] == 42

    def test_postgresql_operations_with_sample_data(self, postgres_connection, sample_data):
        """Test PostgreSQL operations with sample data."""
        cursor = postgres_connection.cursor()
        
        # Create test table
        cursor.execute("""
            CREATE TEMPORARY TABLE sample_table (
                id INTEGER PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                active BOOLEAN
            )
        """)
        
        # Insert sample data
        test_records = sample_data["test_records"]
        for record in test_records:
            cursor.execute(
                "INSERT INTO sample_table (id, name, active) VALUES (%s, %s, %s)",
                (record["id"], record["name"], record["active"])
            )
        
        # Test filtering
        cursor.execute("SELECT COUNT(*) FROM sample_table WHERE active = TRUE")
        active_count = cursor.fetchone()[0]
        assert active_count == 2
        
        # Test update
        cursor.execute(
            "UPDATE sample_table SET name = %s WHERE id = %s",
            ("Updated Test Item 1", 1)
        )
        
        cursor.execute("SELECT name FROM sample_table WHERE id = %s", (1,))
        updated_name = cursor.fetchone()[0]
        assert updated_name == "Updated Test Item 1"

{%- if cookiecutter.use_async == "yes" %}
    @pytest.mark.asyncio
    async def test_async_postgresql_connection(self, async_postgres_connection):
        """Test async PostgreSQL connection and operations."""
        # Create test table
        await async_postgres_connection.execute("""
            CREATE TEMPORARY TABLE async_test_table (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                value INTEGER
            )
        """)
        
        # Test async insert
        row_id = await async_postgres_connection.fetchval(
            "INSERT INTO async_test_table (name, value) VALUES ($1, $2) RETURNING id",
            "async_test", 100
        )
        assert row_id is not None
        
        # Test async select
        row = await async_postgres_connection.fetchrow(
            "SELECT name, value FROM async_test_table WHERE id = $1", row_id
        )
        assert row is not None
        assert row["name"] == "async_test"
        assert row["value"] == 100

    @pytest.mark.asyncio
    async def test_concurrent_postgresql_operations(self, async_postgres_connection):
        """Test concurrent PostgreSQL operations."""
        # Create test table
        await async_postgres_connection.execute("""
            CREATE TEMPORARY TABLE concurrent_test_table (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            )
        """)
        
        # Create multiple concurrent insert operations
        async def insert_record(name: str):
            return await async_postgres_connection.fetchval(
                "INSERT INTO concurrent_test_table (name) VALUES ($1) RETURNING id",
                name
            )
        
        # Run concurrent inserts
        tasks = [insert_record(f"record_{i}") for i in range(5)]
        results = await asyncio.gather(*tasks)
        
        # Verify all inserts succeeded
        assert len(results) == 5
        assert all(result is not None for result in results)
        
        # Verify all records exist
        count = await async_postgres_connection.fetchval(
            "SELECT COUNT(*) FROM concurrent_test_table"
        )
        assert count == 5
{%- endif %}
{%- endif %}


@pytest.mark.integration
class TestEndToEndWorkflows:
    """Test complete end-to-end workflows."""

    def test_basic_workflow(self, sample_data):
        """Test a basic end-to-end workflow."""
        # This is a placeholder for actual workflow testing
        # Replace with real functionality from your package
        
        test_records = sample_data["test_records"]
        assert len(test_records) == 3
        
        # Example workflow: process all active records
        active_records = [r for r in test_records if r["active"]]
        assert len(active_records) == 2

{%- if cookiecutter.use_async == "yes" %}
    @pytest.mark.asyncio
    async def test_async_workflow(self, sample_data):
        """Test an async end-to-end workflow."""
        # This is a placeholder for actual async workflow testing
        # Replace with real functionality from your package
        
        async def process_record(record):
            # Simulate async processing
            await asyncio.sleep(0.01)
            return {**record, "processed": True}
        
        test_records = sample_data["test_records"]
        processed_records = await asyncio.gather(
            *[process_record(record) for record in test_records]
        )
        
        assert len(processed_records) == 3
        assert all(record["processed"] for record in processed_records)
{%- endif %}
{%- else -%}
"""
Integration tests for {{ cookiecutter.project_name }}.
These tests would require external dependencies.
"""

import pytest

import {{ cookiecutter.package_name }}


@pytest.mark.integration
class TestBasicIntegration:
    """Test basic integration functionality."""

    def test_integration_placeholder(self):
        """Placeholder integration test."""
        # Add actual integration tests here when you have external dependencies
        assert {{ cookiecutter.package_name }} is not None

{%- if cookiecutter.use_async == "yes" %}
    @pytest.mark.asyncio
    async def test_async_integration_placeholder(self):
        """Placeholder async integration test."""
        # Add actual async integration tests here
        assert {{ cookiecutter.package_name }} is not None
{%- endif %}
{%- endif -%}