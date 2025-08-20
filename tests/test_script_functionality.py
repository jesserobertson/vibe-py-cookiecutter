"""
Test the sh-based script functionality specifically.
"""

import subprocess
import sys

import pytest


def test_utils_module_generation(cookies, default_context):
    """Test that utils.py is generated with correct sh-based functionality."""
    result = cookies.bake(extra_context=default_context)
    project_dir = result.project_path
    utils_path = project_dir / "scripts" / "utils.py"

    assert utils_path.exists()
    utils_content = utils_path.read_text()

    # Check for sh import
    assert "import sh" in utils_content

    # Check for CommandResult class
    assert "class CommandResult:" in utils_content

    # Check for run_command function
    assert "def run_command(" in utils_content

    # Ensure subprocess is not used
    assert "subprocess" not in utils_content


def test_scripts_use_utils(cookies, default_context):
    """Test that all scripts import and use utils module instead of subprocess."""
    result = cookies.bake(extra_context=default_context)
    project_dir = result.project_path
    scripts_dir = project_dir / "scripts"

    script_files = ["quality.py", "test.py", "build.py", "dev.py", "docs.py"]

    for script_file in script_files:
        script_path = scripts_dir / script_file
        assert script_path.exists()

        script_content = script_path.read_text()

        # Should import from utils
        assert "from utils import run_command" in script_content

        # Should not import subprocess
        assert "import subprocess" not in script_content

        # Should not define its own run_command
        assert "def run_command(" not in script_content


def test_database_script_uses_utils(cookies, mongodb_context):
    """Test that database scripts also use utils when generated."""
    result = cookies.bake(extra_context=mongodb_context)
    project_dir = result.project_path
    test_db_path = project_dir / "scripts" / "test_db.py"

    if test_db_path.exists():
        script_content = test_db_path.read_text()

        # Should import from utils
        assert "from utils import run_command" in script_content

        # Should not import subprocess
        assert "import subprocess" not in script_content

        # Should use result.success instead of result.returncode == 0
        assert "result.success" in script_content
        assert "result.returncode == 0" not in script_content


@pytest.mark.integration
def test_utils_module_syntax(cookies, default_context, command_runner):
    """Test that the generated utils.py has valid syntax and imports."""
    result = cookies.bake(extra_context=default_context)
    project_dir = result.project_path
    utils_path = project_dir / "scripts" / "utils.py"

    # Test syntax by attempting to compile
    with open(utils_path, "rb") as f:
        compile(f.read(), utils_path, "exec")

    # Test that we can import it
    try:
        import_cmd = [
            sys.executable,
            "-c",
            f"import sys; sys.path.insert(0, '{project_dir}/scripts'); import utils",
        ]
        import_result = command_runner(project_dir, import_cmd)
        assert import_result.returncode == 0
    except ImportError:
        pytest.skip("sh library not available for import test")


@pytest.mark.integration
def test_script_help_with_sh(cookies, default_context, command_runner):
    """Test that scripts work with sh library dependency."""
    result = cookies.bake(extra_context=default_context)
    project_dir = result.project_path

    # Skip if pixi is not available
    try:
        subprocess.run(["pixi", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pytest.skip("pixi not available")

    # Install dependencies (including sh)
    install_result = command_runner(project_dir, ["pixi", "install"])
    assert install_result.returncode == 0

    # Test that scripts can run with sh dependency
    script_help_result = command_runner(
        project_dir, ["pixi", "run", "quality", "--help"]
    )
    assert script_help_result.returncode == 0


def test_sh_dependency_in_pixi(cookies, default_context):
    """Test that sh library is properly added to pixi.toml."""
    result = cookies.bake(extra_context=default_context)
    project_dir = result.project_path
    pixi_path = project_dir / "pixi.toml"

    pixi_content = pixi_path.read_text()

    # Check that sh dependency is present
    assert 'sh = ">=2.0.0,<3"' in pixi_content


def test_command_result_interface(cookies, default_context):
    """Test that CommandResult class has the expected interface."""
    result = cookies.bake(extra_context=default_context)
    project_dir = result.project_path
    utils_path = project_dir / "scripts" / "utils.py"

    utils_content = utils_path.read_text()

    # Check CommandResult class structure
    assert "class CommandResult:" in utils_content
    assert "def __init__(self, returncode: int = 0" in utils_content
    assert "def success(self) -> bool:" in utils_content
    assert "return self.returncode == 0" in utils_content

    # Check that it has stdout and stderr attributes
    assert "self.stdout = stdout" in utils_content
    assert "self.stderr = stderr" in utils_content


def test_run_command_error_handling(cookies, default_context):
    """Test that run_command has proper error handling for sh library."""
    result = cookies.bake(extra_context=default_context)
    project_dir = result.project_path
    utils_path = project_dir / "scripts" / "utils.py"

    utils_content = utils_path.read_text()

    # Check for sh.ErrorReturnCode exception handling
    assert "sh.ErrorReturnCode" in utils_content

    # Check for command not found handling
    assert "AttributeError" in utils_content
    assert "Command not found" in utils_content

    # Check for proper error logging
    assert "console.print" in utils_content
    assert "❌" in utils_content


def test_hyphen_command_handling(cookies, default_context):
    """Test that commands with hyphens are handled correctly."""
    result = cookies.bake(extra_context=default_context)
    project_dir = result.project_path
    utils_path = project_dir / "scripts" / "utils.py"

    utils_content = utils_path.read_text()

    # Check for hyphen to underscore conversion
    assert "command_attr = command_name.replace('-', '_')" in utils_content
    assert "getattr(sh, command_attr)" in utils_content


@pytest.mark.integration
def test_pixi_commands_with_sh_scripts(cookies, minimal_context, command_runner):
    """Test that pixi commands work with sh-based scripts."""
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

    # Test various pixi commands that use our sh-based scripts
    commands_to_test = [
        ["pixi", "run", "dev", "status"],
        ["pixi", "run", "build", "status"],
        ["pixi", "run", "docs", "status"],
    ]

    for cmd in commands_to_test:
        result = command_runner(project_dir, cmd)
        # Commands may fail but shouldn't crash with import errors
        assert "ModuleNotFoundError" not in result.stderr
        assert "ImportError" not in result.stderr


def test_backward_compatibility_removed(cookies, default_context):
    """Test that old subprocess patterns are completely removed."""
    result = cookies.bake(extra_context=default_context)
    project_dir = result.project_path
    scripts_dir = project_dir / "scripts"

    # Check all Python files in scripts directory
    for py_file in scripts_dir.glob("*.py"):
        content = py_file.read_text()

        # Should not contain subprocess imports or usage
        assert "import subprocess" not in content
        assert "subprocess.run" not in content
        assert "subprocess.CalledProcessError" not in content
        assert "subprocess.CompletedProcess" not in content

        # Should not contain old return code patterns (except in utils.py)
        if py_file.name != "utils.py":
            # Allow result.returncode in comments but not in actual code
            lines = content.split("\n")
            code_lines = [line for line in lines if not line.strip().startswith("#")]
            code_content = "\n".join(code_lines)
            assert "result.returncode" not in code_content
