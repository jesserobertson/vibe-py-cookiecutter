"""
Test configuration and fixtures for cookiecutter template testing.
"""

import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict

import pytest


@pytest.fixture
def template_dir() -> Path:
    """Return the path to the cookiecutter template directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def default_context() -> Dict[str, Any]:
    """Default context for cookiecutter template generation."""
    return {
        "project_name": "Test Project",
        "project_slug": "test-project",
        "project_description": "A test project generated from cookiecutter",
        "package_name": "test_project",
        "author_name": "Test Author",
        "author_email": "test@example.com",
        "github_username": "testuser",
        "version": "0.1.0",
        "python_version": "3.12",
        "use_async": "yes",
        "use_logerr": "yes",
        "use_hypothesis": "yes",
        "database_backend": "none",
        "include_docker": "no",
        "documentation_tool": "mkdocs-material",
        "license": "MIT",
    }


@pytest.fixture
def mongodb_context(default_context: Dict[str, Any]) -> Dict[str, Any]:
    """Context for testing MongoDB integration."""
    context = default_context.copy()
    context.update({"database_backend": "mongodb", "include_docker": "yes"})
    return context


@pytest.fixture
def postgresql_context(default_context: Dict[str, Any]) -> Dict[str, Any]:
    """Context for testing PostgreSQL integration."""
    context = default_context.copy()
    context.update({"database_backend": "postgresql", "include_docker": "yes"})
    return context


@pytest.fixture
def minimal_context(default_context: Dict[str, Any]) -> Dict[str, Any]:
    """Minimal context for testing basic functionality."""
    context = default_context.copy()
    context.update(
        {
            "use_async": "no",
            "use_logerr": "no",
            "use_hypothesis": "no",
            "database_backend": "none",
            "include_docker": "no",
            "documentation_tool": "mkdocs-material",
        }
    )
    return context


def run_command_in_dir(
    directory: Path, command: list[str], check: bool = True
) -> subprocess.CompletedProcess:
    """Run a command in the specified directory."""
    return subprocess.run(
        command, cwd=directory, capture_output=True, text=True, check=check
    )


@pytest.fixture
def command_runner():
    """Fixture that provides a command runner for testing generated projects."""
    return run_command_in_dir


@pytest.fixture
def temp_dir():
    """Provide a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "docker: mark test as requiring docker")
