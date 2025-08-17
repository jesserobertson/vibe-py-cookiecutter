"""
Test configuration and fixtures for {{ cookiecutter.project_name }}.
"""

{%- if cookiecutter.use_async == "yes" %}
import asyncio
{%- endif %}
{%- if cookiecutter.database_backend == "mongodb" %}
import os
from typing import Generator
{%- elif cookiecutter.database_backend == "postgresql" %}
import os
from typing import Generator
{%- endif %}

{%- if cookiecutter.use_hypothesis == "yes" %}
from hypothesis import Verbosity, settings
{%- endif %}
{%- if cookiecutter.database_backend == "mongodb" and cookiecutter.use_async == "yes" %}
from motor.motor_asyncio import AsyncIOMotorClient
{%- endif %}
{%- if cookiecutter.database_backend == "postgresql" and cookiecutter.use_async == "yes" %}
import asyncpg
{%- endif %}
{%- if cookiecutter.database_backend == "mongodb" %}
from pymongo import MongoClient
{%- elif cookiecutter.database_backend == "postgresql" %}
import psycopg2
{%- endif %}
import pytest


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="Run integration tests"
    )


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers",
        "integration: mark test as integration test"
    )
{%- if cookiecutter.use_hypothesis == "yes" %}
    config.addinivalue_line(
        "markers",
        "hypothesis: mark test as property-based test"
    )
{%- endif %}
{%- if cookiecutter.use_async == "yes" %}
    config.addinivalue_line(
        "markers",
        "asyncio: mark test as async test"
    )
{%- endif %}


def pytest_collection_modifyitems(config, items):
    """Modify test collection to handle markers."""
    if config.getoption("--run-integration"):
        # Run all tests including integration
        return

    # Skip integration tests by default
    skip_integration = pytest.mark.skip(reason="need --run-integration option to run")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_integration)


{%- if cookiecutter.use_async == "yes" %}
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
{%- endif %}


{%- if cookiecutter.database_backend == "mongodb" %}
@pytest.fixture(scope="session")
def mongodb_uri() -> str:
    """Get MongoDB connection URI for testing."""
    return os.getenv("MONGODB_URI", "mongodb://localhost:27017")


@pytest.fixture(scope="session")
def test_database_name() -> str:
    """Get test database name."""
    return "{{ cookiecutter.package_name }}_test"


@pytest.fixture(scope="function")
def mongodb_client(mongodb_uri: str) -> Generator[MongoClient, None, None]:
    """Create a MongoDB client for testing."""
    client = MongoClient(mongodb_uri)
    try:
        # Test connection
        client.admin.command('ping')
        yield client
    except Exception as e:
        pytest.skip(f"MongoDB not available: {e}")
    finally:
        client.close()


@pytest.fixture(scope="function")
def test_collection(mongodb_client: MongoClient, test_database_name: str):
    """Create a test collection and clean up after test."""
    db = mongodb_client[test_database_name]
    collection_name = "test_collection"
    collection = db[collection_name]

    # Clean up before test
    collection.delete_many({})

    yield collection

    # Clean up after test
    collection.delete_many({})


{%- if cookiecutter.use_async == "yes" %}
@pytest.fixture(scope="function")
async def async_mongodb_client(mongodb_uri: str) -> AsyncIOMotorClient:
    """Create an async MongoDB client for testing."""
    client = AsyncIOMotorClient(mongodb_uri)
    try:
        # Test connection
        await client.admin.command('ping')
        yield client
    except Exception as e:
        pytest.skip(f"MongoDB not available: {e}")
    finally:
        client.close()


@pytest.fixture(scope="function")
async def async_test_collection(async_mongodb_client: AsyncIOMotorClient, test_database_name: str):
    """Create an async test collection and clean up after test."""
    db = async_mongodb_client[test_database_name]
    collection_name = "test_collection"
    collection = db[collection_name]

    # Clean up before test
    await collection.delete_many({})

    yield collection

    # Clean up after test
    await collection.delete_many({})
{%- endif %}

{%- elif cookiecutter.database_backend == "postgresql" %}
@pytest.fixture(scope="session")
def postgres_dsn() -> str:
    """Get PostgreSQL connection DSN for testing."""
    return os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/{{ cookiecutter.package_name }}_test")


@pytest.fixture(scope="function")
def postgres_connection(postgres_dsn: str):
    """Create a PostgreSQL connection for testing."""
    try:
        conn = psycopg2.connect(postgres_dsn)
        conn.autocommit = True
        yield conn
    except Exception as e:
        pytest.skip(f"PostgreSQL not available: {e}")
    finally:
        if 'conn' in locals():
            conn.close()


{%- if cookiecutter.use_async == "yes" %}
@pytest.fixture(scope="function")
async def async_postgres_connection(postgres_dsn: str):
    """Create an async PostgreSQL connection for testing."""
    try:
        conn = await asyncpg.connect(postgres_dsn)
        yield conn
    except Exception as e:
        pytest.skip(f"PostgreSQL not available: {e}")
    finally:
        if 'conn' in locals():
            await conn.close()
{%- endif %}
{%- endif %}


@pytest.fixture
def sample_data():
    """Provide sample data for testing."""
    return {
        "test_records": [
            {"id": 1, "name": "Test Item 1", "active": True},
            {"id": 2, "name": "Test Item 2", "active": False},
            {"id": 3, "name": "Test Item 3", "active": True},
        ]
    }


{%- if cookiecutter.use_hypothesis == "yes" %}
# Configure hypothesis for testing
settings.register_profile("dev", max_examples=10, verbosity=Verbosity.verbose)
settings.register_profile("ci", max_examples=100, deadline=1000)
settings.load_profile("dev")
{%- endif %}
