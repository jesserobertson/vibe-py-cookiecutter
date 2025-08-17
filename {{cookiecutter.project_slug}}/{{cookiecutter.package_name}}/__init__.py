"""
{{ cookiecutter.project_name }} - {{ cookiecutter.project_description }}

{{ cookiecutter.project_name }} is a modern Python {{ cookiecutter.python_version }}+ library that follows
best practices for code quality, testing, and maintainability.

Example:
    Basic usage example:

    ```python
    import {{ cookiecutter.package_name }}

    # Your code here
    ```

{%- if cookiecutter.use_async == "yes" %}

    Async usage example:

    ```python
    import asyncio
    import {{ cookiecutter.package_name }}

    async def main():
        # Your async code here
        pass

    asyncio.run(main())
    ```
{%- endif %}
"""

__version__ = "{{ cookiecutter.version }}"
__author__ = "{{ cookiecutter.author_name }}"
__email__ = "{{ cookiecutter.author_email }}"

# Define public API
__all__ = [
    "__author__",
    "__email__",
    "__version__",
]


class {{ cookiecutter.package_name.title().replace('_', '') }}Error(Exception):
    """Base exception class for {{ cookiecutter.project_name }}."""
    pass


class {{ cookiecutter.package_name.title().replace('_', '') }}ConfigError({{ cookiecutter.package_name.title().replace('_', '') }}Error):
    """Raised when there's a configuration error."""
    pass


{%- if cookiecutter.database_backend != "none" %}
class {{ cookiecutter.package_name.title().replace('_', '') }}DatabaseError({{ cookiecutter.package_name.title().replace('_', '') }}Error):
    """Raised when there's a database-related error."""
    pass
{%- endif %}


# Add exception classes to public API
__all__.extend([
    "{{ cookiecutter.package_name.title().replace('_', '') }}ConfigError",
{%- if cookiecutter.database_backend != "none" %}
    "{{ cookiecutter.package_name.title().replace('_', '') }}DatabaseError",
{%- endif %}
    "{{ cookiecutter.package_name.title().replace('_', '') }}Error",
])


# Import main functionality
# TODO: Import your main classes and functions here
# Example:
# from .core import MainClass, main_function
# __all__.extend(["MainClass", "main_function"])

# Lazy imports for optional dependencies
def _get_version() -> str:
    """Get the package version."""
    return __version__


# Package initialization
def _initialize_package() -> None:
    """Initialize the package with any necessary setup."""
    # TODO: Add any package initialization logic here
    pass


# Initialize the package when imported
_initialize_package()
