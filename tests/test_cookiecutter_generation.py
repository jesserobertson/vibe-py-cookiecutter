"""
Test cookiecutter template generation with different configurations.
"""

import json

import pytest


def test_default_generation(cookies, default_context):
    """Test generating cookiecutter with default context."""
    result = cookies.bake(extra_context=default_context)

    assert result.exit_code == 0
    assert result.exception is None

    project_dir = result.project_path
    assert project_dir.is_dir()
    assert (project_dir / "pyproject.toml").exists()
    assert (project_dir / "pixi.toml").exists()
    assert (project_dir / "README.md").exists()
    assert (project_dir / "CLAUDE.md").exists()


def test_minimal_generation(cookies, minimal_context):
    """Test generating minimal cookiecutter without optional features."""
    result = cookies.bake(extra_context=minimal_context)

    assert result.exit_code == 0
    assert result.exception is None

    project_dir = result.project_path
    assert project_dir.is_dir()

    # Check that optional features are not included
    pixi_content = (project_dir / "pixi.toml").read_text()
    assert "logerr" not in pixi_content
    assert "hypothesis" not in pixi_content
    assert "pytest-asyncio" not in pixi_content


def test_mongodb_generation(cookies, mongodb_context):
    """Test generating cookiecutter with MongoDB integration."""
    result = cookies.bake(extra_context=mongodb_context)

    assert result.exit_code == 0
    assert result.exception is None

    project_dir = result.project_path
    assert project_dir.is_dir()

    # Check MongoDB-specific files and configuration
    assert (project_dir / "infrastructure" / "docker-compose.test.yml").exists()
    assert (project_dir / "infrastructure" / "test-data" / "init_mongodb.py").exists()

    pixi_content = (project_dir / "pixi.toml").read_text()
    assert "pymongo" in pixi_content
    assert "motor" in pixi_content  # async MongoDB driver


def test_postgresql_generation(cookies, postgresql_context):
    """Test generating cookiecutter with PostgreSQL integration."""
    result = cookies.bake(extra_context=postgresql_context)

    assert result.exit_code == 0
    assert result.exception is None

    project_dir = result.project_path
    assert project_dir.is_dir()

    # Check PostgreSQL-specific files and configuration
    assert (project_dir / "infrastructure" / "docker-compose.test.yml").exists()
    assert (
        project_dir / "infrastructure" / "test-data" / "init_postgresql.py"
    ).exists()

    pixi_content = (project_dir / "pixi.toml").read_text()
    assert "psycopg2" in pixi_content
    assert "asyncpg" in pixi_content  # async PostgreSQL driver


def test_project_structure(cookies, default_context):
    """Test that generated project has correct structure."""
    result = cookies.bake(extra_context=default_context)

    project_dir = result.project_path
    package_name = default_context["package_name"]

    # Core project files
    assert (project_dir / "pyproject.toml").exists()
    assert (project_dir / "pixi.toml").exists()
    assert (project_dir / "README.md").exists()
    assert (project_dir / "CLAUDE.md").exists()
    assert (project_dir / "LICENSE").exists()

    # Package structure
    package_dir = project_dir / package_name
    assert package_dir.is_dir()
    assert (package_dir / "__init__.py").exists()
    assert (package_dir / "py.typed").exists()

    # Scripts directory
    scripts_dir = project_dir / "scripts"
    assert scripts_dir.is_dir()
    assert (scripts_dir / "utils.py").exists()
    assert (scripts_dir / "quality.py").exists()
    assert (scripts_dir / "test.py").exists()
    assert (scripts_dir / "build.py").exists()
    assert (scripts_dir / "dev.py").exists()
    assert (scripts_dir / "docs.py").exists()

    # Tests directory
    tests_dir = project_dir / "tests"
    assert tests_dir.is_dir()
    assert (tests_dir / "conftest.py").exists()
    assert (tests_dir / "unit").is_dir()
    assert (tests_dir / "integration").is_dir()

    # Documentation
    docs_dir = project_dir / "docs"
    assert docs_dir.is_dir()
    assert (docs_dir / "content").is_dir()
    assert (docs_dir / "mkdocs.yml").exists()


def test_pixi_configuration(cookies, default_context):
    """Test that pixi.toml is correctly configured."""
    result = cookies.bake(extra_context=default_context)

    project_dir = result.project_path
    pixi_path = project_dir / "pixi.toml"
    pixi_content = pixi_path.read_text()

    # Check for our custom sh dependency
    assert "sh = " in pixi_content

    # Check for unified scripts
    assert 'quality = { cmd = "python scripts/quality.py"' in pixi_content
    assert 'test = { cmd = "python scripts/test.py"' in pixi_content
    assert 'build = { cmd = "python scripts/build.py"' in pixi_content
    assert 'dev = { cmd = "python scripts/dev.py"' in pixi_content
    assert 'docs = { cmd = "python scripts/docs.py"' in pixi_content

    # Check unified operations
    assert "clean =" in pixi_content
    assert "check-all =" in pixi_content


def test_script_imports(cookies, default_context):
    """Test that all scripts correctly import from utils."""
    result = cookies.bake(extra_context=default_context)

    project_dir = result.project_path
    scripts_dir = project_dir / "scripts"

    script_files = [
        "quality.py",
        "test.py",
        "build.py",
        "dev.py",
        "docs.py",
        "test_db.py",
    ]

    for script_file in script_files:
        script_path = scripts_dir / script_file
        if (
            script_path.exists() and script_path.stat().st_size > 0
        ):  # test_db.py may be empty with no database
            script_content = script_path.read_text()
            assert "from utils import run_command" in script_content
            assert (
                "subprocess" not in script_content
            )  # Ensure subprocess is not imported


def test_claude_md_content(cookies, default_context):
    """Test that CLAUDE.md is properly generated with project-specific content."""
    result = cookies.bake(extra_context=default_context)

    project_dir = result.project_path
    claude_md = project_dir / "CLAUDE.md"
    content = claude_md.read_text()

    # Check for project-specific values
    assert default_context["project_name"] in content
    assert default_context["project_description"] in content
    assert default_context["package_name"] in content

    # Check for documentation of new sh-based approach
    assert "unified task scripts" in content.lower()
    assert "pixi run" in content


@pytest.mark.parametrize(
    "license_type", ["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause"]
)
def test_different_licenses(cookies, default_context, license_type):
    """Test generation with different license types."""
    context = default_context.copy()
    context["license"] = license_type

    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    project_dir = result.project_path
    license_file = project_dir / "LICENSE"

    assert license_file.exists()
    license_content = license_file.read_text()

    # Basic check that license content matches expected type
    if license_type == "MIT":
        assert "MIT License" in license_content
    elif license_type == "Apache-2.0":
        assert "Apache License" in license_content
    elif license_type == "GPL-3.0":
        assert "GNU GENERAL PUBLIC LICENSE" in license_content
    elif license_type == "BSD-3-Clause":
        assert "BSD 3-Clause License" in license_content


def test_cookiecutter_json_validity(template_dir):
    """Test that cookiecutter.json is valid JSON with expected structure."""
    cookiecutter_json = template_dir / "cookiecutter.json"
    assert cookiecutter_json.exists()

    with open(cookiecutter_json) as f:
        config = json.load(f)

    # Check required fields
    required_fields = [
        "project_name",
        "project_slug",
        "project_description",
        "package_name",
        "author_name",
        "author_email",
        "github_username",
        "version",
        "python_version",
    ]

    for field in required_fields:
        assert field in config

    # Check choice fields have valid options (they are lists with default first)
    assert isinstance(config["use_async"], list) and config["use_async"][0] in [
        "yes",
        "no",
    ]
    assert isinstance(config["use_logerr"], list) and config["use_logerr"][0] in [
        "yes",
        "no",
    ]
    assert isinstance(config["use_hypothesis"], list) and config["use_hypothesis"][
        0
    ] in ["yes", "no"]
    assert isinstance(config["database_backend"], list) and config["database_backend"][
        0
    ] in ["none", "mongodb", "postgresql", "sqlite"]
    assert isinstance(config["include_docker"], list) and config["include_docker"][
        0
    ] in ["yes", "no"]
    assert isinstance(config["documentation_tool"], list) and config[
        "documentation_tool"
    ][0] in ["mkdocs-material", "sphinx"]
