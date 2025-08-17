# Quick Start

Get up and running with {{ cookiecutter.project_name }} in minutes.

## Installation

```bash
pip install {{ cookiecutter.package_name }}
```

## Basic Usage

Here's a simple example to get you started:

```python
import {{ cookiecutter.package_name }}

# Basic example
def main():
    print("Hello from {{ cookiecutter.project_name }}!")

if __name__ == "__main__":
    main()
```

{%- if cookiecutter.use_async == "yes" %}

## Async Usage

{{ cookiecutter.project_name }} supports both synchronous and asynchronous operations:

```python
import asyncio
import {{ cookiecutter.package_name }}

async def async_example():
    """Example of asynchronous usage."""
    print("Async hello from {{ cookiecutter.project_name }}!")

async def main():
    await async_example()

if __name__ == "__main__":
    asyncio.run(main())
```
{%- endif %}

{%- if cookiecutter.database_backend != "none" %}

## Database Integration

{{ cookiecutter.project_name }} provides seamless {{ cookiecutter.database_backend }} integration:

{%- if cookiecutter.database_backend == "mongodb" %}
```python
import {{ cookiecutter.package_name }}

# Connect to MongoDB
connection_string = "mongodb://localhost:27017"
database_name = "my_database"
collection_name = "my_collection"

# Basic database operations
def database_example():
    # Your database code here
    pass

if __name__ == "__main__":
    database_example()
```

{%- if cookiecutter.use_async == "yes" %}
### Async Database Operations

```python
import asyncio
import {{ cookiecutter.package_name }}

async def async_database_example():
    """Example of async database operations."""
    connection_string = "mongodb://localhost:27017"
    database_name = "my_database"
    collection_name = "my_collection"
    
    # Your async database code here
    pass

if __name__ == "__main__":
    asyncio.run(async_database_example())
```
{%- endif %}

{%- elif cookiecutter.database_backend == "postgresql" %}
```python
import {{ cookiecutter.package_name }}

# Connect to PostgreSQL
connection_string = "postgresql://user:password@localhost:5432/mydatabase"

# Basic database operations
def database_example():
    # Your database code here
    pass

if __name__ == "__main__":
    database_example()
```

{%- if cookiecutter.use_async == "yes" %}
### Async Database Operations

```python
import asyncio
import {{ cookiecutter.package_name }}

async def async_database_example():
    """Example of async database operations."""
    connection_string = "postgresql://user:password@localhost:5432/mydatabase"
    
    # Your async database code here
    pass

if __name__ == "__main__":
    asyncio.run(async_database_example())
```
{%- endif %}
{%- endif %}
{%- endif %}

## Configuration

{{ cookiecutter.project_name }} can be configured through environment variables or direct parameters:

```python
import os
import {{ cookiecutter.package_name }}

# Environment-based configuration
{%- if cookiecutter.database_backend == "mongodb" %}
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
{%- elif cookiecutter.database_backend == "postgresql" %}
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/db")
{%- endif %}

# Use configuration in your application
def configured_example():
    # Your configured code here
    pass
```

## Error Handling

{{ cookiecutter.project_name }} uses modern Python error handling patterns:

```python
import {{ cookiecutter.package_name }}

def error_handling_example():
    try:
        # Your code that might raise exceptions
        pass
    except {{ cookiecutter.package_name }}.{{ cookiecutter.package_name.title() }}Error as e:
        print(f"{{ cookiecutter.project_name }} error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    error_handling_example()
```

## Next Steps

Now that you have the basics working:

1. **Read the [User Guide](concepts.md)** - Learn about core concepts and advanced features
2. **Check out [Examples](examples.md)** - See more comprehensive examples
3. **Browse the [API Reference](api/index.md)** - Detailed documentation of all functions and classes
{%- if cookiecutter.database_backend != "none" %}
4. **Learn about [Database Integration](database.md)** - Deep dive into {{ cookiecutter.database_backend }} features
{%- endif %}

## Getting Help

- **Documentation**: Continue reading the documentation for detailed guides
- **Issues**: Report bugs or request features on [GitHub Issues](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/issues)
- **Discussions**: Join the conversation in [GitHub Discussions](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/discussions)

Happy coding with {{ cookiecutter.project_name }}! 🚀