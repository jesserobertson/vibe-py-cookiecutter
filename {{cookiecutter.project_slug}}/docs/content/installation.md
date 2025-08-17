# Installation

## Requirements

- Python {{ cookiecutter.python_version }}+
{%- if cookiecutter.database_backend == "mongodb" %}
- MongoDB (for database features)
{%- elif cookiecutter.database_backend == "postgresql" %}
- PostgreSQL (for database features)
{%- endif %}

## Install from PyPI

The recommended way to install {{ cookiecutter.project_name }} is from PyPI using pip:

```bash
pip install {{ cookiecutter.package_name }}
```

## Optional Dependencies

{{ cookiecutter.project_name }} supports several optional dependencies for additional functionality:

{%- if cookiecutter.database_backend != "none" %}
### Database Support

For {{ cookiecutter.database_backend }} support:

```bash
pip install {{ cookiecutter.package_name }}[database]
```
{%- endif %}

### Development Dependencies

If you want to contribute to the project or run tests:

```bash
pip install {{ cookiecutter.package_name }}[dev]
```

### Documentation Dependencies

To build documentation locally:

```bash
pip install {{ cookiecutter.package_name }}[docs]
```

### All Dependencies

To install all optional dependencies:

```bash
pip install {{ cookiecutter.package_name }}[all]
```

## Development Installation

If you want to contribute to {{ cookiecutter.project_name }}, you can install it in development mode:

### Prerequisites

1. Install [pixi](https://pixi.sh) package manager
2. Clone the repository:

```bash
git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git
cd {{ cookiecutter.project_slug }}
```

### Setup Development Environment

```bash
# Install dependencies
pixi install

# Set up development environment (pre-commit hooks, etc.)
pixi run dev setup

# Run tests to verify installation
pixi run test unit
```

## Verify Installation

To verify that {{ cookiecutter.project_name }} is installed correctly:

```python
import {{ cookiecutter.package_name }}
print({{ cookiecutter.package_name }}.__version__)
```

{%- if cookiecutter.database_backend != "none" %}

## Database Setup

### {{ cookiecutter.database_backend.title() }} Configuration

{%- if cookiecutter.database_backend == "mongodb" %}
Make sure MongoDB is running and accessible. You can install MongoDB locally or use a cloud service like MongoDB Atlas.

Default connection string format:
```
mongodb://localhost:27017
```
{%- elif cookiecutter.database_backend == "postgresql" %}
Make sure PostgreSQL is running and accessible. You can install PostgreSQL locally or use a cloud service.

Default connection string format:
```
postgresql://username:password@localhost:5432/database
```
{%- endif %}

### Testing Database Setup

For development and testing, you can use Docker:

```bash
# Start test database
pixi run test db start

# Check database status
pixi run test db status

# Stop test database
pixi run test db stop
```
{%- endif %}

## Troubleshooting

### Common Issues

1. **Import Error**: Make sure you've installed {{ cookiecutter.package_name }} in the correct Python environment.

2. **Version Conflicts**: Try installing in a fresh virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install {{ cookiecutter.package_name }}
   ```

{%- if cookiecutter.database_backend != "none" %}
3. **Database Connection Issues**: Verify that your {{ cookiecutter.database_backend }} server is running and accessible.
{%- endif %}

### Getting Help

If you encounter any issues during installation:

1. Check the [Issue Tracker](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/issues)
2. Search for existing solutions
3. Create a new issue if needed