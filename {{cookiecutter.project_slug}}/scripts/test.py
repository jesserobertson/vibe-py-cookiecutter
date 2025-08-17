#!/usr/bin/env python3
"""
Testing management script with pytest{% if cookiecutter.database_backend != 'none' %} and database support{% endif %}.
Unified interface for all testing tasks including unit, integration{% if cookiecutter.database_backend != 'none' %}, and database management{% endif %}.
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.status import Status

{%- if cookiecutter.database_backend != 'none' %}
# Import database management functionality
sys.path.append(str(Path(__file__).parent))
{%- if cookiecutter.include_docker == 'yes' %}
from test_db import (
    is_database_ready, wait_for_database, run_init_script,
    COMPOSE_FILE, DB_CONTAINER
)
{%- endif %}
{%- endif %}

app = typer.Typer(
    name="test",
    help="Testing Management Script",
    add_completion=False,
)

{%- if cookiecutter.database_backend != 'none' %}
# Create database management subgroup
db_app = typer.Typer(name="db", help="Database management commands")
app.add_typer(db_app, name="db")
{%- endif %}

console = Console()

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
TESTS_DIR = PROJECT_ROOT / "tests"
DOCS_DIR = PROJECT_ROOT / "docs"


def run_command(cmd: list[str], capture_output: bool = False, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command with proper error handling."""
    try:
        if capture_output:
            return subprocess.run(cmd, capture_output=True, text=True, check=check, cwd=PROJECT_ROOT)
        else:
            return subprocess.run(cmd, check=check, cwd=PROJECT_ROOT)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]❌ Command failed: {' '.join(cmd)}[/red]")
        if capture_output and e.stdout:
            console.print(f"[yellow]STDOUT: {e.stdout}[/yellow]")
        if capture_output and e.stderr:
            console.print(f"[red]STDERR: {e.stderr}[/red]")
        raise typer.Exit(1)


@app.command()
def unit(
    coverage: bool = typer.Option(True, "--coverage/--no-coverage", help="Generate coverage report"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    fail_fast: bool = typer.Option(False, "--fail-fast", "-x", help="Stop on first failure")
) -> None:
    """Run unit tests."""
    panel = Panel.fit("🧪 Running Unit Tests", style="blue")
    console.print(panel)
    
    cmd = ["pytest", "tests/unit/"]
    
    if verbose:
        cmd.append("-v")
    if fail_fast:
        cmd.append("-x")
    if coverage:
        cmd.extend(["--cov={{ cookiecutter.package_name }}", "--cov-report=term", "--cov-report=xml", "--cov-report=html"])
    
    with Status("Running unit tests...", console=console, spinner="dots"):
        run_command(cmd)
    
    console.print("[green]✅ Unit tests completed![/green]")


{%- if cookiecutter.database_backend != 'none' %}
@app.command()
def integration(
    coverage: bool = typer.Option(True, "--coverage/--no-coverage", help="Generate coverage report"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
) -> None:
    """Run integration tests (requires test database)."""
    panel = Panel.fit("🔗 Running Integration Tests", style="blue")
    console.print(panel)
    
{%- if cookiecutter.include_docker == 'yes' %}
    # Ensure test database is ready
    console.print("🔄 Ensuring test database is ready...")
    run_command(["python", "scripts/test_db.py", "ensure"])
{%- endif %}
    
    cmd = ["pytest", "tests/integration/", "--run-integration"]
    
    if verbose:
        cmd.append("-v")
    if coverage:
        cmd.extend(["--cov={{ cookiecutter.package_name }}", "--cov-report=term", "--cov-report=xml", "--cov-report=html"])
    
    with Status("Running integration tests...", console=console, spinner="dots"):
        run_command(cmd)
    
    console.print("[green]✅ Integration tests completed![/green]")
{%- endif %}


@app.command()
def all(
    coverage: bool = typer.Option(True, "--coverage/--no-coverage", help="Generate coverage report"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
) -> None:
    """Run all tests (unit{% if cookiecutter.database_backend != 'none' %} + integration{% endif %}{% if cookiecutter.documentation_tool == 'mkdocs-material' %} + docs{% endif %})."""
    panel = Panel.fit("🚀 Running All Tests", style="blue")
    console.print(panel)
    
{%- if cookiecutter.database_backend != 'none' and cookiecutter.include_docker == 'yes' %}
    # Ensure test database is ready
    console.print("🔄 Ensuring test database is ready...")
    run_command(["python", "scripts/test_db.py", "ensure"])
{%- endif %}
    
    cmd = [
        "pytest", "tests/", 
{%- if cookiecutter.database_backend != 'none' %}
        "--run-integration", 
{%- endif %}
{%- if cookiecutter.documentation_tool == 'mkdocs-material' %}
        "--doctest-glob='*.md'", "docs/content/"
{%- endif %}
    ]
    
    if verbose:
        cmd.append("-v")
    if coverage:
        cmd.extend(["--cov={{ cookiecutter.package_name }}", "--cov-report=term", "--cov-report=xml", "--cov-report=html"])
    
    with Status("Running all tests...", console=console, spinner="dots"):
        run_command(cmd)
    
    console.print("[green]✅ All tests completed![/green]")


{%- if cookiecutter.database_backend != 'none' and cookiecutter.include_docker == 'yes' %}
# Database management commands
@db_app.command()
def start() -> None:
    """Start {{ cookiecutter.database_backend }} test container."""
    panel = Panel.fit("🚀 Starting {{ cookiecutter.database_backend.title() }} Test Environment", style="blue")
    console.print(panel)
    
    with Status("Starting container...", console=console, spinner="bouncingBar"):
        run_command(["docker-compose", "-f", COMPOSE_FILE, "up", "-d"])
    
    if wait_for_database():
        try:
            run_init_script()
            console.print("[green]✅ {{ cookiecutter.database_backend.title() }} test environment ready![/green]")
        except Exception as e:
            console.print(f"[red]❌ Failed to initialize database: {e}[/red]")
            raise typer.Exit(1)
    else:
        raise typer.Exit(1)


@db_app.command()
def stop() -> None:
    """Stop {{ cookiecutter.database_backend }} test container."""
    console.print("🛑 Stopping {{ cookiecutter.database_backend }} test container...")
    run_command(["docker-compose", "-f", COMPOSE_FILE, "down"])
    console.print("[green]✅ {{ cookiecutter.database_backend.title() }} test container stopped[/green]")


@db_app.command()
def status() -> None:
    """Show database status."""
    panel = Panel.fit("📊 {{ cookiecutter.database_backend.title() }} Test Environment Status", style="cyan")
    console.print(panel)
    
    # Use the existing test_db.py status functionality
    run_command(["python", "scripts/test_db.py", "status"])


@db_app.command()
def ensure() -> None:
    """Ensure {{ cookiecutter.database_backend }} is running and ready for tests."""
    try:
        # Check if already healthy
        result = run_command(["python", "scripts/test_db.py", "healthcheck"], check=False)
        if result.returncode == 0:
            console.print("✅ {{ cookiecutter.database_backend.title() }} test database is already healthy")
            return
    except Exception:
        pass
    
    # Not healthy, so start it
    console.print("🔄 Starting {{ cookiecutter.database_backend }} test database...")
    start()
{%- endif %}


@app.command()
def clean() -> None:
    """Clean test artifacts (coverage reports, pytest cache, etc.)."""
    console.print("🧹 Cleaning test artifacts...")
    
    artifacts_cleaned = []
    
    # Clean coverage reports
    coverage_dirs = [PROJECT_ROOT / "htmlcov", PROJECT_ROOT / ".coverage"]
    for path in coverage_dirs:
        if path.exists():
            if path.is_dir():
                import shutil
                shutil.rmtree(path)
                artifacts_cleaned.append(f"Coverage directory: {path.name}")
            else:
                path.unlink()
                artifacts_cleaned.append(f"Coverage file: {path.name}")
    
    # Clean pytest cache
    pytest_cache = PROJECT_ROOT / ".pytest_cache"
    if pytest_cache.exists():
        import shutil
        shutil.rmtree(pytest_cache)
        artifacts_cleaned.append("Pytest cache")
    
    # Clean any .pyc files and __pycache__ directories
    for pyc_file in PROJECT_ROOT.rglob("*.pyc"):
        pyc_file.unlink()
        artifacts_cleaned.append(f"Compiled Python file: {pyc_file.name}")
    
    pycache_dirs = list(PROJECT_ROOT.rglob("__pycache__"))
    for pycache_dir in pycache_dirs:
        if pycache_dir.is_dir():
            import shutil
            shutil.rmtree(pycache_dir)
            artifacts_cleaned.append(f"Python cache: {pycache_dir}")
    
    if artifacts_cleaned:
        console.print("[green]✅ Cleaned test artifacts:[/green]")
        for artifact in artifacts_cleaned:
            console.print(f"  • {artifact}")
    else:
        console.print("[yellow]⚠️ No test artifacts to clean[/yellow]")


if __name__ == "__main__":
    # Change to project root directory
    import os
    os.chdir(PROJECT_ROOT)
    app()