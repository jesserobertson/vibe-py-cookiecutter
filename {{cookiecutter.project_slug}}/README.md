# {{ cookiecutter.project_name }}

[![CI](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/workflows/CI/badge.svg)](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/actions)
[![codecov](https://codecov.io/gh/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/branch/main/graph/badge.svg)](https://codecov.io/gh/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }})
[![PyPI version](https://badge.fury.io/py/{{ cookiecutter.package_name }}.svg)](https://badge.fury.io/py/{{ cookiecutter.package_name }})
[![Python {{ cookiecutter.python_version }}+](https://img.shields.io/badge/python-{{ cookiecutter.python_version }}+-blue.svg)](https://www.python.org/downloads/)
{%- if cookiecutter.documentation_tool == "mkdocs-material" %}
[![Documentation](https://img.shields.io/badge/docs-mkdocs-blue.svg)](https://{{ cookiecutter.github_username }}.github.io/{{ cookiecutter.project_slug }})
{%- endif %}
[![License: {{ cookiecutter.license }}](https://img.shields.io/badge/License-{{ cookiecutter.license }}-yellow.svg)](LICENSE)

{{ cookiecutter.project_description }}

## Features

- 🚀 **Modern Python {{ cookiecutter.python_version }}+** with comprehensive type hints
- 📦 **Unified Development Experience** with pixi task management
- 🧪 **Comprehensive Testing** with pytest{% if cookiecutter.use_hypothesis == "yes" %} and hypothesis{% endif %}
- 🔍 **Code Quality Enforcement** with ruff and mypy (100% compliance)
{%- if cookiecutter.use_async == "yes" %}
- ⚡ **Async Support** with both synchronous and asynchronous APIs
{%- endif %}
{%- if cookiecutter.database_backend != "none" %}
- 🗄️ **{{ cookiecutter.database_backend.title() }} Integration**{% if cookiecutter.use_async == "yes" %} with async support{% endif %}
{%- endif %}
{%- if cookiecutter.documentation_tool == "mkdocs-material" %}
- 📚 **Beautiful Documentation** with MkDocs Material
{%- endif %}
- 🔒 **Security Scanning** and dependency management
- 🤖 **Automated CI/CD** with GitHub Actions

## Quick Start

### Installation

```bash
pip install {{ cookiecutter.package_name }}
```

### Basic Usage

```python
import {{ cookiecutter.package_name }}

# Your code here
print("Hello from {{ cookiecutter.project_name }}!")
```

{%- if cookiecutter.use_async == "yes" %}

### Async Usage

```python
import asyncio
import {{ cookiecutter.package_name }}

async def main():
    # Your async code here
    print("Async hello from {{ cookiecutter.project_name }}!")

asyncio.run(main())
```
{%- endif %}

{%- if cookiecutter.database_backend != "none" %}

### Database Integration

{%- if cookiecutter.database_backend == "mongodb" %}
```python
import {{ cookiecutter.package_name }}

# MongoDB integration
connection_string = "mongodb://localhost:27017"
# Your database code here
```
{%- elif cookiecutter.database_backend == "postgresql" %}
```python
import {{ cookiecutter.package_name }}

# PostgreSQL integration  
connection_string = "postgresql://user:password@localhost:5432/mydatabase"
# Your database code here
```
{%- endif %}
{%- endif %}

## Installation Options

### Basic Installation

```bash
pip install {{ cookiecutter.package_name }}
```

### Development Installation

For contributors and developers:

```bash
# Install pixi (if not already installed)
curl -fsSL https://pixi.sh/install.sh | bash

# Clone and set up the project
git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git
cd {{ cookiecutter.project_slug }}

# Install dependencies and set up development environment
pixi install
pixi run dev setup

# Run tests to verify installation
pixi run test unit
```

{%- if cookiecutter.database_backend != "none" %}

### Optional Dependencies

{%- if cookiecutter.database_backend == "mongodb" %}
For MongoDB support:
```bash
pip install {{ cookiecutter.package_name }}[mongodb]
```
{%- elif cookiecutter.database_backend == "postgresql" %}
For PostgreSQL support:
```bash
pip install {{ cookiecutter.package_name }}[postgresql]
```
{%- endif %}

For development:
```bash
pip install {{ cookiecutter.package_name }}[dev]
```

For documentation:
```bash
pip install {{ cookiecutter.package_name }}[docs]
```

For everything:
```bash
pip install {{ cookiecutter.package_name }}[all]
```
{%- endif %}

## Development

This project uses modern Python development practices with comprehensive tooling:

### Development Commands

```bash
# Testing
pixi run test unit                 # Run unit tests
{%- if cookiecutter.database_backend != "none" %}
pixi run test integration          # Run integration tests  
pixi run test all                  # Run all tests
{%- if cookiecutter.include_docker == "yes" %}
pixi run test db start             # Start test database
{%- endif %}
{%- endif %}

# Code Quality  
pixi run quality check             # Run all quality checks
pixi run quality fix               # Auto-fix issues

# Documentation
pixi run docs serve                # Serve docs locally
pixi run docs build                # Build documentation

# Build & Distribution
pixi run build package             # Build package
pixi run build check               # Check package

# Development Environment
pixi run dev setup                 # Set up dev environment
pixi run dev status                # Show environment status
```

### Code Quality Standards

This project maintains **100% ruff compliance** and comprehensive type coverage:

- **Formatting**: Automated with ruff
- **Linting**: Strict ruff configuration with modern Python rules
- **Type Checking**: Full mypy coverage with strict settings
- **Testing**: Comprehensive test suite with coverage reporting
{%- if cookiecutter.use_hypothesis == "yes" %}
- **Property Testing**: Hypothesis for robust edge case testing
{%- endif %}

### Contributing

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/{{ cookiecutter.project_slug }}.git
   cd {{ cookiecutter.project_slug }}
   ```
3. **Set up development environment**:
   ```bash
   pixi install
   pixi run dev setup
   ```
4. **Create a feature branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```
5. **Make your changes** and ensure all tests pass:
   ```bash
   pixi run check-all
   ```
6. **Commit your changes**:
   ```bash
   git commit -m "Add amazing feature"
   ```
7. **Push to your fork**:
   ```bash
   git push origin feature/amazing-feature
   ```
8. **Create a Pull Request** on GitHub

## Documentation

{%- if cookiecutter.documentation_tool == "mkdocs-material" %}
- **[Full Documentation](https://{{ cookiecutter.github_username }}.github.io/{{ cookiecutter.project_slug }})** - Comprehensive guides and API reference
{%- endif %}
- **[Installation Guide](docs/content/installation.md)** - Detailed installation instructions
- **[Quick Start](docs/content/quickstart.md)** - Get up and running quickly
- **[API Reference](docs/content/api/)** - Complete API documentation
{%- if cookiecutter.database_backend != "none" %}
- **[Database Integration](docs/content/database.md)** - {{ cookiecutter.database_backend.title() }} integration guide
{%- endif %}

### Building Documentation Locally

```bash
# Serve documentation with live reload
pixi run docs serve

# Build static documentation
pixi run docs build
```

## Requirements

- **Python {{ cookiecutter.python_version }}+**
{%- if cookiecutter.database_backend == "mongodb" %}
- **MongoDB** (for database features)
{%- elif cookiecutter.database_backend == "postgresql" %}
- **PostgreSQL** (for database features)
{%- endif %}
{%- if cookiecutter.include_docker == "yes" and cookiecutter.database_backend != "none" %}
- **Docker** (for development database)
{%- endif %}

## License

This project is licensed under the {{ cookiecutter.license }} License - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: https://{{ cookiecutter.github_username }}.github.io/{{ cookiecutter.project_slug }}
- **Issues**: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/issues
- **Discussions**: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/discussions

## Acknowledgments

- Built with [pixi](https://pixi.sh) for modern Python dependency management
- Tested with [pytest](https://pytest.org){% if cookiecutter.use_hypothesis == "yes" %} and [hypothesis](https://hypothesis.readthedocs.io){% endif %}
- Documentation powered by [MkDocs](https://mkdocs.org){% if cookiecutter.documentation_tool == "mkdocs-material" %} with [Material theme](https://squidfunk.github.io/mkdocs-material/){% endif %}
- Code quality enforced by [ruff](https://docs.astral.sh/ruff/) and [mypy](https://mypy.readthedocs.io)

---

Made with ❤️ by [{{ cookiecutter.author_name }}](https://github.com/{{ cookiecutter.github_username }})