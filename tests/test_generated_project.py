"""
Test the functionality of generated projects.
"""

import subprocess
import sys

import pytest


@pytest.mark.integration
def test_pixi_install_works(cookies, default_context, command_runner):
    """Test that pixi install works in generated project."""
    result = cookies.bake(extra_context=default_context)
    project_dir = result.project_path

    # Skip if pixi is not available
    try:
        subprocess.run(["pixi", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pytest.skip("pixi not available")

    # Test pixi install
    install_result = command_runner(project_dir, ["pixi", "install"])
    assert install_result.returncode == 0


@pytest.mark.integration
def test_python_syntax_validation(cookies, default_context):
    """Test that all generated Python files have valid syntax."""
    result = cookies.bake(extra_context=default_context)
    project_dir = result.project_path

    # Find all Python files
    python_files = list(project_dir.rglob("*.py"))
    assert len(python_files) > 0

    for py_file in python_files:
        # Compile each file to check syntax
        try:
            with open(py_file, "rb") as f:
                compile(f.read(), py_file, "exec")
        except SyntaxError as e:
            pytest.fail(f"Syntax error in {py_file}: {e}")


def test_package_imports(cookies, default_context, command_runner):
    """Test that the generated package can be imported."""
    result = cookies.bake(extra_context=default_context)
    project_dir = result.project_path
    package_name = default_context["package_name"]

    # Try to import the package
    import_cmd = [
        sys.executable,
        "-c",
        f"import sys; sys.path.insert(0, '.'); import {package_name}",
    ]

    import_result = command_runner(project_dir, import_cmd)
    assert import_result.returncode == 0


def test_script_help_commands(cookies, default_context, command_runner):
    """Test that all scripts respond to --help."""
    result = cookies.bake(extra_context=default_context)
    project_dir = result.project_path
    scripts_dir = project_dir / "scripts"

    script_files = ["quality.py", "test.py", "build.py", "dev.py", "docs.py"]

    for script_file in script_files:
        script_path = scripts_dir / script_file
        if script_path.exists():
            help_result = command_runner(
                project_dir, [sys.executable, str(script_path), "--help"]
            )
            assert help_result.returncode == 0
            assert (
                "Usage:" in help_result.stdout or "help" in help_result.stdout.lower()
            )


@pytest.mark.integration
def test_quality_checks_with_pixi(cookies, minimal_context, command_runner):
    """Test that quality checks can run via pixi using unified scripts."""
    result = cookies.bake(extra_context=minimal_context)
    project_dir = result.project_path

    # Skip if pixi is not available
    try:
        subprocess.run(["pixi", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pytest.skip("pixi not available")

    # Install dependencies first
    install_result = command_runner(project_dir, ["pixi", "install"])
    assert install_result.returncode == 0

    # Test unified quality check command (format check only, as it's fastest)
    format_result = command_runner(
        project_dir, ["pixi", "run", "quality", "format", "--check"]
    )
    # May fail due to formatting issues, but should not crash
    assert format_result.returncode in [0, 1]


def test_readme_generation(cookies, default_context):
    """Test that README.md is properly generated."""
    result = cookies.bake(extra_context=default_context)
    project_dir = result.project_path
    readme_path = project_dir / "README.md"

    assert readme_path.exists()
    readme_content = readme_path.read_text()

    # Check for project-specific content
    assert default_context["project_name"] in readme_content
    assert default_context["project_description"] in readme_content
    assert default_context["author_name"] in readme_content

    # Check for essential sections
    assert "# " in readme_content  # At least one heading
    assert "## " in readme_content  # At least one subheading
    assert "install" in readme_content.lower()


def test_pyproject_toml_validity(cookies, default_context):
    """Test that generated pyproject.toml is valid."""
    result = cookies.bake(extra_context=default_context)
    project_dir = result.project_path
    pyproject_path = project_dir / "pyproject.toml"

    assert pyproject_path.exists()

    # Try to parse with tomllib (Python 3.11+) or fallback
    try:
        import tomllib

        with open(pyproject_path, "rb") as f:
            config = tomllib.load(f)
    except ImportError:
        # Fallback for older Python versions
        try:
            import tomli

            with open(pyproject_path, "rb") as f:
                config = tomli.load(f)
        except ImportError:
            # Skip TOML validation if no parser available
            return

    # Check essential sections
    assert "build-system" in config
    assert "project" in config
    assert "tool" in config

    # Check project metadata
    project = config["project"]
    assert "name" in project
    assert "version" in project
    assert "description" in project
    assert project["name"] == default_context["package_name"]


@pytest.mark.integration
def test_basic_tests_run(cookies, minimal_context, command_runner):
    """Test that basic unit tests can run in generated project."""
    result = cookies.bake(extra_context=minimal_context)
    project_dir = result.project_path

    # Skip if pixi is not available
    try:
        subprocess.run(["pixi", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pytest.skip("pixi not available")

    # Install dependencies
    install_result = command_runner(project_dir, ["pixi", "install"])
    assert install_result.returncode == 0

    # Run basic unit tests using unified test script
    test_result = command_runner(
        project_dir, ["pixi", "run", "test", "unit", "--no-coverage"]
    )
    # Tests should pass (returncode 0) or be skipped but not crash
    assert test_result.returncode in [0, 5]  # 0 = pass, 5 = no tests collected


def test_documentation_structure(cookies, default_context):
    """Test that documentation structure is properly created."""
    result = cookies.bake(extra_context=default_context)
    project_dir = result.project_path
    docs_dir = project_dir / "docs"

    assert docs_dir.exists()
    assert (docs_dir / "content").exists()
    assert (docs_dir / "mkdocs.yml").exists()

    # Check for basic documentation files
    content_dir = docs_dir / "content"
    assert (content_dir / "index.md").exists()
    assert (content_dir / "installation.md").exists()
    assert (content_dir / "quickstart.md").exists()


def test_license_file_content(cookies, default_context):
    """Test that LICENSE file contains appropriate content."""
    result = cookies.bake(extra_context=default_context)
    project_dir = result.project_path
    license_path = project_dir / "LICENSE"

    assert license_path.exists()
    license_content = license_path.read_text()

    # Check for author name and year
    assert default_context["author_name"] in license_content
    assert "2024" in license_content or "2025" in license_content


@pytest.mark.slow
@pytest.mark.integration
def test_full_project_workflow(cookies, minimal_context, command_runner):
    """Test a complete workflow: install, format, lint, test."""
    result = cookies.bake(extra_context=minimal_context)
    project_dir = result.project_path

    # Skip if pixi is not available
    try:
        subprocess.run(["pixi", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pytest.skip("pixi not available")

    # 1. Install dependencies
    install_result = command_runner(project_dir, ["pixi", "install"])
    assert install_result.returncode == 0

    # 2. Format code
    format_result = command_runner(project_dir, ["pixi", "run", "quality", "format"])
    assert format_result.returncode == 0

    # 3. Check formatting
    format_check_result = command_runner(
        project_dir, ["pixi", "run", "quality", "format", "--check"]
    )
    assert format_check_result.returncode == 0

    # 4. Run linting (may fail but shouldn't crash)
    lint_result = command_runner(project_dir, ["pixi", "run", "quality", "lint"])
    assert lint_result.returncode in [0, 1]

    # 5. Run tests
    test_result = command_runner(
        project_dir, ["pixi", "run", "test", "unit", "--no-coverage"]
    )
    assert test_result.returncode in [0, 5]
