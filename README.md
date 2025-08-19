# Modern Python Project Template

A comprehensive cookiecutter template for modern Python projects with unified development tooling and best practices.

## Features

🚀 **Modern Python 3.12+** with comprehensive type hints and modern syntax

📦 **Unified Development Experience** with pixi task management

🧪 **Comprehensive Testing** with pytest, hypothesis, and async support

🔍 **Code Quality Enforcement** with ruff, mypy (100% compliance required)

⚡ **Optional Async Support** for high-performance applications

🗄️ **Database Integration** (MongoDB, PostgreSQL, SQLite options)

📚 **Beautiful Documentation** with MkDocs Material

🔒 **Security Scanning** with bandit and safety

🤖 **Automated CI/CD** with GitHub Actions

📋 **Claude Code Integration** with comprehensive CLAUDE.md

## Quick Start

### Install Cookiecutter

```bash
pip install cookiecutter
```

### Generate Project

```bash
cookiecutter https://github.com/jesserobertson/vibe-py-cookiecutter
```

### Setup Development Environment

```bash
cd your-new-project

# Install pixi if not already installed
curl -fsSL https://pixi.sh/install.sh | bash

# Install dependencies and setup environment
pixi install
pixi run dev setup

# Verify installation
pixi run test unit
pixi run quality check
```

## Template Options

The template supports various configuration options:

- **Project Information**: Name, description, author details
- **Python Version**: Defaults to 3.12
- **Async Support**: Optional asyncio integration
- **Database Backend**: MongoDB, PostgreSQL, SQLite, or none
- **Testing Framework**: Pytest with optional Hypothesis
- **Error Handling**: Optional logerr for Rust-like Result/Option types
- **Documentation**: MkDocs Material or Sphinx
- **License**: MIT, Apache-2.0, BSD-3-Clause, GPL-3.0, or Proprietary
- **Docker Support**: Optional containerization for databases

## Generated Project Structure

```
your-project/
├── your_package/              # Main package
│   ├── __init__.py           # Package initialization with versioning
│   └── py.typed              # PEP 561 type marker
├── tests/                    # Comprehensive test suite
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests (optional)
│   └── conftest.py          # Test configuration
├── docs/                     # Documentation
│   ├── content/             # Documentation content
│   └── mkdocs.yml           # MkDocs configuration
├── scripts/                  # Unified development scripts
│   ├── quality.py           # Code quality management
│   ├── test.py              # Testing management
│   ├── build.py             # Build and distribution
│   ├── docs.py              # Documentation management
│   └── dev.py               # Development environment
├── infrastructure/           # Docker and test data (optional)
├── .github/workflows/        # CI/CD workflows
├── pixi.toml                # Pixi configuration
├── pyproject.toml           # Python project configuration
├── CLAUDE.md                # Claude Code guidance
└── README.md                # Project documentation
```

## Development Workflow

The generated project includes unified development commands:

```bash
# Testing
pixi run test unit                 # Unit tests
pixi run test integration          # Integration tests (if enabled)
pixi run test all                  # All tests

# Code Quality (100% compliance required)
pixi run quality check             # All quality checks
pixi run quality fix               # Auto-fix issues

# Documentation
pixi run docs serve                # Serve docs locally
pixi run docs build                # Build documentation

# Build & Distribution
pixi run build package             # Build package
pixi run build upload              # Upload to PyPI

# Development Environment
pixi run dev setup                 # Setup pre-commit hooks
pixi run dev status                # Environment status
```

## Key Features Explained

### Unified Development Scripts

All development tasks use the same commands locally and in CI/CD:
- **Local**: `pixi run quality check`
- **CI/CD**: `pixi run quality check`

This eliminates "works on my machine" problems.

### 100% Code Quality Compliance

The template enforces strict code quality:
- **Ruff**: Modern Python linting and formatting
- **MyPy**: Comprehensive type checking
- **Pre-commit**: Automated quality checks
- **No exceptions**: All quality checks must pass

### Modern Python 3.12+ Features

- Union syntax: `str | int` instead of `Union[str, int]`
- Built-in generics: `list[str]` instead of `List[str]`
- Pattern matching with `match` statements
- Modern type annotations throughout

### Optional Database Integration

Choose from:
- **MongoDB**: With pymongo (sync) and motor (async)
- **PostgreSQL**: With psycopg2 (sync) and asyncpg (async)
- **SQLite**: Built-in Python support
- **None**: Pure Python project

### Comprehensive Testing

- **Unit Tests**: Fast, isolated tests
- **Integration Tests**: Database and external service tests
- **Property-Based Testing**: Hypothesis for edge cases
- **Async Testing**: Full pytest-asyncio support
- **Coverage Reporting**: HTML and XML reports

### Claude Code Integration

Generated projects include comprehensive `CLAUDE.md` files with:
- Project architecture and patterns
- Development workflows and commands
- Code quality standards and practices
- Security guidelines
- Modern Python typing requirements

## CI/CD Integration

The template includes GitHub Actions workflows for:
- **Continuous Integration**: Testing and quality checks
- **Security Scanning**: Dependency vulnerability scanning  
- **Documentation**: Automated docs builds and deployment
- **Release Management**: Automated PyPI publishing

## Requirements

- **Python 3.12+**
- **Pixi** package manager
- **Docker** (optional, for database testing)
- **Git** for version control

## License

This template is licensed under the MIT License. Generated projects can use any supported license.

## Template Testing

This cookiecutter template includes a comprehensive testing harness using pytest-cookies.

### Install Test Dependencies

```bash
# Using pixi (recommended)
pixi install

# Or using pip
pip install -e .[test]
```

### Run Template Tests

```bash
# Run all tests
pixi run test all

# Run only fast tests (skip integration/slow tests)
pixi run test fast

# Run integration tests
pixi run test integration

# Run specific test categories
pixi run test generation    # Cookiecutter generation tests
pixi run test scripts      # Script functionality tests

# Check code quality
pixi run quality check     # All quality checks
pixi run quality lint      # Linting only
pixi run quality format --check  # Format checking
```

### Test Categories

- **Generation Tests**: Test cookiecutter template generation with different configurations
- **Project Functionality Tests**: Test that generated projects work correctly  
- **Script Functionality Tests**: Test the sh-based script functionality specifically

The testing harness validates:
- ✅ Template generation with various configurations
- ✅ Generated project structure and file existence
- ✅ Python syntax validation of all generated files
- ✅ Script functionality with sh library integration
- ✅ Integration workflows (install, format, lint, test)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the template tests:
   ```bash
   pixi run test all
   pixi run quality check
   ```
5. Test manual generation:
   ```bash
   cookiecutter . --no-input
   cd my-awesome-project
   pixi install
   pixi run check-all
   ```
6. Submit a pull request

## Acknowledgments

This template incorporates best practices from the Python community and is designed to work seamlessly with modern development tools and Claude Code.

---

**Generate your next Python project with modern best practices built-in!** 🚀