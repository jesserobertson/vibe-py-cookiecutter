# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

{{ cookiecutter.project_name }} is {{ cookiecutter.project_description }}. It follows modern Python development practices with comprehensive tooling and unified development workflows.

**Key Features:**
- Modern Python {{ cookiecutter.python_version }}+ with comprehensive type hints
- Unified development experience with pixi task management
- Comprehensive testing with pytest{% if cookiecutter.use_hypothesis == "yes" %} and hypothesis{% endif %}
- Code quality enforcement with ruff and mypy (100% compliance required)
{%- if cookiecutter.use_async == "yes" %}
- Both synchronous and asynchronous APIs
{%- endif %}
{%- if cookiecutter.database_backend != "none" %}
- {{ cookiecutter.database_backend.title() }} integration{% if cookiecutter.use_async == "yes" %} with async support{% endif %}
{%- endif %}
{%- if cookiecutter.documentation_tool == "mkdocs-material" %}
- Beautiful documentation with MkDocs Material
{%- endif %}
- Automated CI/CD with GitHub Actions
- Security scanning and dependency management

## Development Commands

Use `pixi` with unified task scripts for all development tasks:

### **Core Unified Scripts**
```bash
# Testing (unit{% if cookiecutter.database_backend != "none" %}, integration, database management{% endif %})
pixi run test --help               # Show all test commands
pixi run test unit                 # Run unit tests with coverage
{%- if cookiecutter.database_backend != "none" %}
pixi run test integration          # Run integration tests (auto-starts DB)
pixi run test all                  # Run all tests (unit + integration{% if cookiecutter.documentation_tool == 'mkdocs-material' %} + docs{% endif %})
{%- if cookiecutter.include_docker == 'yes' %}
pixi run test db start             # Start test database
pixi run test db status            # Check database status
pixi run test db stop              # Stop test database
{%- endif %}
{%- else %}
pixi run test all                  # Run all tests{% if cookiecutter.documentation_tool == 'mkdocs-material' %} (unit + docs){% endif %}
{%- endif %}
pixi run test clean                # Clean test artifacts

# Code Quality (linting, formatting, type checking)
pixi run quality --help            # Show all quality commands
pixi run quality check             # Run all quality checks (MUST pass 100%)
pixi run quality typecheck         # Run mypy type checking
pixi run quality format            # Format code with ruff
pixi run quality lint              # Run ruff linting
pixi run quality fix               # Auto-fix all possible issues

# Development Environment
pixi run dev --help               # Show all dev commands
pixi run dev setup                # Install pre-commit hooks
pixi run dev status               # Show development environment status
pixi run dev clean                # Clean development artifacts

# Build & Distribution
pixi run build --help             # Show all build commands
pixi run build package            # Build wheel and source distribution
pixi run build status             # Show build status and information
pixi run build clean              # Clean build artifacts

# Documentation
pixi run docs --help              # Show all docs commands
pixi run docs serve               # Serve documentation locally
pixi run docs build               # Build documentation
pixi run docs status              # Show documentation status
pixi run docs clean               # Clean documentation build
```

### **Unified Operations**
```bash
# Unified clean (all artifacts)
pixi run clean                    # Clean test + docs + build + dev artifacts

# Comprehensive checks (all tests + quality)
pixi run check-all                # Run all tests + quality checks
```

## Architecture & Philosophy

### Core Principles
- **Modern Python patterns**: Use Python {{ cookiecutter.python_version }}+ features and type hints
- **Unified development experience**: Local commands match CI/CD exactly
- **Quality enforcement**: 100% ruff compliance, comprehensive mypy typing
- **Comprehensive testing**: Unit tests{% if cookiecutter.database_backend != "none" %}, integration tests{% endif %}{% if cookiecutter.use_hypothesis == "yes" %}, property-based testing{% endif %}
{%- if cookiecutter.use_async == "yes" %}
- **Async-first design**: Support both sync and async APIs where appropriate
{%- endif %}
- **Documentation-driven**: Keep docs up-to-date and comprehensive
- **Security-conscious**: Regular dependency scanning and security checks

### Project Structure
```
{{ cookiecutter.project_slug }}/
├── {{ cookiecutter.package_name }}/         # Main package  
│   ├── __init__.py            # Package initialization
│   ├── py.typed               # PEP 561 type marker
{%- if cookiecutter.use_async == "yes" %}
│   ├── sync/                  # Synchronous operations
│   ├── async/                 # Asynchronous operations  
{%- endif %}
{%- if cookiecutter.database_backend != "none" %}
│   ├── database/              # Database integration
{%- endif %}
│   └── utils/                 # Utility functions
├── tests/                     # Test suite
│   ├── unit/                  # Unit tests
{%- if cookiecutter.database_backend != "none" %}
│   ├── integration/           # Integration tests
{%- endif %}
│   └── conftest.py            # Test configuration
├── docs/                      # Documentation
│   ├── content/               # Documentation content
{%- if cookiecutter.documentation_tool == "mkdocs-material" %}
│   └── mkdocs.yml             # MkDocs configuration
{%- endif %}
├── scripts/                   # Unified development scripts
{%- if cookiecutter.database_backend != "none" and cookiecutter.include_docker == "yes" %}
├── infrastructure/            # Docker and test data
│   ├── docker-compose.test.yml
│   └── test-data/
{%- endif %}
└── .github/workflows/         # CI/CD workflows
```

### API Design Principles
- **Explicit over implicit**: Clear function signatures and parameters
- **Type safety first**: Full mypy coverage with strict settings
- **Error handling**: Proper exception handling and informative error messages
{%- if cookiecutter.use_async == "yes" %}
- **Async compatibility**: Consistent APIs between sync and async versions
{%- endif %}
- **Documentation**: Comprehensive docstrings with examples
- **Testing**: Every public function should have comprehensive tests

## Modern Python {{ cookiecutter.python_version }}+ Typing Requirements

**This project targets Python {{ cookiecutter.python_version }}+ and MUST use modern typing syntax:**

- **Use union syntax**: `A | B` instead of `Union[A, B]`
- **Use built-in generics**: `list[str]`, `dict[str, Any]` instead of `List[str]`, `Dict[str, Any]`
- **Use modern optional syntax**: `T | None` instead of `Optional[T]`
- **Use new type statement**: `type MyType = int | str` instead of `MyType: TypeAlias = Union[int, str]`
- **Minimal typing imports**: Only import what you actually need
- **Use match statements**: Prefer pattern matching over if/elif chains where appropriate

**Examples of correct modern typing:**
```python
# ✅ Modern (Python {{ cookiecutter.python_version }}+)
type UserId = int | str
type ConfigDict = dict[str, Any]
type ItemList = list[dict[str, Any]]

def process_items(
    items: ItemList,
    user_id: UserId | None = None,
    config: ConfigDict | None = None
) -> bool:
    match result:
        case Success(data):
            return process_success(data)
        case Error(msg):
            return handle_error(msg)
```

**Examples of deprecated syntax (DO NOT USE):**
```python
# ❌ Old style (Python < {{ cookiecutter.python_version }})
from typing import Union, List, Dict, Optional, TypeAlias

UserIdType: TypeAlias = Union[int, str]
ConfigDict = Dict[str, Any]
ItemList = List[Dict[str, Any]]

def process_items(
    items: ItemList,
    user_id: Optional[UserIdType] = None,
    config: Optional[Dict[str, str]] = None
) -> bool:
    if result.is_ok():
        return process_success(result.value)
    else:
        return handle_error(result.error)
```

## Development Practices

### Code Quality Standards
- **MANDATORY**: Maintain 100% ruff compliance - all ruff checks must pass before committing
- Always run `pixi run check-all` before committing changes
- Use pre-commit hooks for automated quality checks: `pixi run dev setup`
- Maintain 100% type coverage with mypy
- Write comprehensive tests with good coverage

### Ruff Compliance Standards
This project enforces **100% ruff compliance** with no exceptions. All code must pass:

```bash
# These commands must return "All checks passed!"
pixi run quality check             # Runs all quality checks
pixi run quality lint              # Linting compliance  
pixi run quality format --check    # Formatting compliance
```

**Key ruff rules enforced:**
- **No unused arguments (ARG001)**: All function parameters must be used
- **Proper variable binding**: Correct closure handling in lambdas
- **Boolean simplification**: Use direct boolean evaluation instead of `== True`
- **Absolute imports**: Use absolute imports instead of relative imports
- **Clean formatting**: No trailing whitespace or formatting inconsistencies

**Code quality workflow:**
1. Write code following project patterns
2. Run `pixi run quality check` to verify compliance
3. Fix any ruff issues before committing
4. Commit only when all checks pass

**When ruff issues arise:**
- **Auto-fix when possible**: Run `pixi run quality fix` to automatically resolve fixable issues
- **Manual fixes required for**: Complex logic issues, unused arguments, variable binding
- **Never ignore rules**: All ruff issues must be resolved, no exceptions

### Testing Strategy
- **Comprehensive coverage**: Aim for high test coverage across all code paths
- **Multiple test types**: Unit tests{% if cookiecutter.database_backend != "none" %}, integration tests{% endif %}{% if cookiecutter.use_hypothesis == "yes" %}, property-based tests{% endif %}
- **Test organization**: Keep tests well-organized and maintainable
{%- if cookiecutter.use_async == "yes" %}
- **Async testing patterns**: Use `pytest-asyncio` with proper async fixtures
{%- endif %}
{%- if cookiecutter.database_backend != "none" %}
- **Database testing**: Use test databases with proper cleanup
{%- endif %}

{%- if cookiecutter.use_async == "yes" %}

### Async Development Practices
- **Use async/await consistently**: Don't mix async and sync operations without proper handling
- **Leverage concurrency**: Use `asyncio.gather()` for concurrent operations when appropriate
- **Handle backpressure**: Use proper flow control to avoid overwhelming resources
- **Test async code properly**: Use `pytest-asyncio` for async test methods
{%- endif %}

{%- if cookiecutter.database_backend != "none" %}

## Database Integration

### {{ cookiecutter.database_backend.title() }} Configuration

{%- if cookiecutter.database_backend == "mongodb" %}
Configure MongoDB connection through environment variables:

```bash
# Development/Testing
export MONGODB_URI="mongodb://localhost:27017"

# Production (example)
export MONGODB_URI="mongodb+srv://user:pass@cluster.mongodb.net/dbname"
```

### Development Database Setup

Use Docker for local development:

```bash
# Start test database with sample data
pixi run test db start

# Check database status  
pixi run test db status

# Stop database
pixi run test db stop
```

{%- elif cookiecutter.database_backend == "postgresql" %}
Configure PostgreSQL connection through environment variables:

```bash
# Development/Testing
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/{{ cookiecutter.package_name }}_test"

# Production (example)
export DATABASE_URL="postgresql://user:pass@host:5432/dbname"
```

### Development Database Setup

Use Docker for local development:

```bash
# Start test database with sample data
pixi run test db start

# Check database status
pixi run test db status

# Stop database  
pixi run test db stop
```
{%- endif %}
{%- endif %}

## Environment Setup

This project uses pixi for dependency management and provides a unified development experience.

**Prerequisites:**
- Python {{ cookiecutter.python_version }}+
- [pixi](https://pixi.sh) package manager
{%- if cookiecutter.include_docker == "yes" and cookiecutter.database_backend != "none" %}
- Docker (for database testing)
{%- endif %}

**Setup:**
```bash
# Clone repository
git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git
cd {{ cookiecutter.project_slug }}

# Install dependencies
pixi install

# Set up development environment
pixi run dev setup

# Verify installation
pixi run test unit
pixi run quality check
```

## Security Guidelines

### Critical Security Rules
- **NEVER commit credentials**: API keys, tokens, passwords, or connection strings must never be committed to git
- **Environment variables**: Use environment variables for sensitive configuration
- **Dependency security**: Regularly check dependencies for vulnerabilities with `pixi run security`
- **Input validation**: Sanitize all user inputs to prevent injection attacks

{%- if cookiecutter.database_backend != "none" %}

### Database Security
- **Connection strings**: Never hardcode database connection strings in code
- **Query sanitization**: Use parameterized queries to prevent injection attacks
- **Authentication**: Implement proper database authentication
- **Error handling**: Don't expose sensitive information in error messages
{%- endif %}

### Development Security Practices
- **Type safety**: Full mypy coverage helps prevent security bugs
- **Logging safety**: Ensure credentials are never logged
- **Dependency pinning**: Use pinned dependency versions to prevent supply chain attacks
- **Pre-commit hooks**: Use automated security scanning before commits

## Adding New Functionality

When adding new features to {{ cookiecutter.project_name }}:

1. **Follow existing patterns**: Look at similar functionality for consistency
2. **Add comprehensive tests**: Include unit tests{% if cookiecutter.database_backend != "none" %} and integration tests{% endif %}
3. **Update documentation**: Add docstrings and update user guides
4. **Type everything**: Ensure full mypy compatibility with modern typing
5. **Run quality checks**: Ensure `pixi run check-all` passes
{%- if cookiecutter.use_async == "yes" %}
6. **Consider async support**: Add async versions for I/O operations
{%- endif %}
7. **Update CLAUDE.md**: Add any new development patterns or requirements

## Deployment & Distribution

### Building for Distribution
```bash
# Build package
pixi run build package

# Check package quality
pixi run build check

# Upload to PyPI (with proper credentials)
pixi run build upload
```

### CI/CD Pipeline
The project uses GitHub Actions for:
- **Continuous Integration**: Automated testing and quality checks
- **Security Scanning**: Dependency vulnerability scanning
- **Documentation**: Automated documentation builds
- **Release Management**: Automated PyPI publishing on releases

All CI/CD operations use the same unified scripts as local development, ensuring consistency between local testing and production deployment.