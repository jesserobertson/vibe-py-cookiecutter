{%- if cookiecutter.database_backend != 'none' and cookiecutter.include_docker == 'yes' -%}
#!/usr/bin/env python3
"""
Database management for testing.
Handles {{ cookiecutter.database_backend }} test container lifecycle.
"""

import sys
import time
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.status import Status

from utils import run_command

app = typer.Typer(
    name="test-db",
    help="{{ cookiecutter.database_backend.title() }} Test Database Management",
    add_completion=False,
)
console = Console()

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
INFRASTRUCTURE_DIR = PROJECT_ROOT / "infrastructure"
COMPOSE_FILE = str(INFRASTRUCTURE_DIR / "docker-compose.test.yml")
{%- if cookiecutter.database_backend == 'mongodb' %}
DB_CONTAINER = "{{ cookiecutter.project_slug.replace('-', '') }}-test-mongodb"
{%- elif cookiecutter.database_backend == 'postgresql' %}
DB_CONTAINER = "{{ cookiecutter.project_slug.replace('-', '') }}-test-postgres"
{%- endif %}




{%- if cookiecutter.database_backend == 'mongodb' %}
def is_mongodb_ready() -> bool:
    """Check if MongoDB is ready to accept connections."""
    try:
        result = run_command([
            "docker", "exec", DB_CONTAINER,
            "mongosh", "--eval", "db.adminCommand('ping')"
        ], capture_output=True, check=False)
        return result.success
    except Exception:
        return False


def wait_for_mongodb(timeout: int = 60) -> bool:
    """Wait for MongoDB to be ready."""
    console.print(f"⏳ Waiting for MongoDB to be ready (timeout: {timeout}s)...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_mongodb_ready():
            console.print("[green]✅ MongoDB is ready![/green]")
            return True
        time.sleep(2)
    
    console.print(f"[red]❌ MongoDB did not become ready within {timeout} seconds[/red]")
    return False
{%- elif cookiecutter.database_backend == 'postgresql' %}
def is_postgres_ready() -> bool:
    """Check if PostgreSQL is ready to accept connections."""
    try:
        result = run_command([
            "docker", "exec", DB_CONTAINER,
            "pg_isready", "-h", "localhost", "-p", "5432"
        ], capture_output=True, check=False)
        return result.success
    except Exception:
        return False


def wait_for_postgres(timeout: int = 60) -> bool:
    """Wait for PostgreSQL to be ready."""
    console.print(f"⏳ Waiting for PostgreSQL to be ready (timeout: {timeout}s)...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_postgres_ready():
            console.print("[green]✅ PostgreSQL is ready![/green]")
            return True
        time.sleep(2)
    
    console.print(f"[red]❌ PostgreSQL did not become ready within {timeout} seconds[/red]")
    return False
{%- endif %}


def run_init_script() -> None:
    """Run database initialization script."""
    init_script = INFRASTRUCTURE_DIR / "test-data" / "init_{{ cookiecutter.database_backend }}.py"
    if init_script.exists():
        console.print("🔄 Running database initialization script...")
        run_command(["python", str(init_script)])
    else:
        console.print("[yellow]⚠️ No initialization script found[/yellow]")


@app.command()
def start() -> None:
    """Start {{ cookiecutter.database_backend }} test container."""
    panel = Panel.fit("🚀 Starting {{ cookiecutter.database_backend.title() }} Test Container", style="blue")
    console.print(panel)
    
    with Status("Starting container...", console=console, spinner="bouncingBar"):
        run_command(["docker-compose", "-f", COMPOSE_FILE, "up", "-d"])
    
{%- if cookiecutter.database_backend == 'mongodb' %}
    if wait_for_mongodb():
{%- elif cookiecutter.database_backend == 'postgresql' %}
    if wait_for_postgres():
{%- endif %}
        try:
            run_init_script()
            console.print("[green]✅ {{ cookiecutter.database_backend.title() }} test environment ready![/green]")
        except Exception as e:
            console.print(f"[red]❌ Failed to initialize database: {e}[/red]")
            raise typer.Exit(1)
    else:
        raise typer.Exit(1)


@app.command()
def stop() -> None:
    """Stop {{ cookiecutter.database_backend }} test container."""
    console.print("🛑 Stopping {{ cookiecutter.database_backend }} test container...")
    run_command(["docker-compose", "-f", COMPOSE_FILE, "down"])
    console.print("[green]✅ {{ cookiecutter.database_backend.title() }} test container stopped[/green]")


@app.command()
def status() -> None:
    """Show database container status."""
    panel = Panel.fit("📊 {{ cookiecutter.database_backend.title() }} Container Status", style="cyan")
    console.print(panel)
    
    try:
        result = run_command(["docker", "ps", "-f", f"name={DB_CONTAINER}", "--format", "table {{ '{{.Names}}' }}\t{{ '{{.Status}}' }}\t{{ '{{.Ports}}' }}"], capture_output=True)
        if result.stdout.strip():
            console.print(result.stdout)
        else:
            console.print("[yellow]⚠️ Container not running[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Failed to get container status: {e}[/red]")


@app.command()
def healthcheck() -> None:
    """Check if database is healthy and ready."""
{%- if cookiecutter.database_backend == 'mongodb' %}
    if is_mongodb_ready():
{%- elif cookiecutter.database_backend == 'postgresql' %}
    if is_postgres_ready():
{%- endif %}
        console.print("[green]✅ {{ cookiecutter.database_backend.title() }} is healthy and ready[/green]")
    else:
        console.print("[red]❌ {{ cookiecutter.database_backend.title() }} is not ready[/red]")
        raise typer.Exit(1)


@app.command()
def ensure() -> None:
    """Ensure database is running and ready for tests."""
    try:
        # Check if already healthy
        result = run_command(["python", __file__, "healthcheck"], check=False)
        if result.success:
            console.print("✅ {{ cookiecutter.database_backend.title() }} test database is already healthy")
            return
    except Exception:
        pass
    
    # Not healthy, so start it
    console.print("🔄 Starting {{ cookiecutter.database_backend }} test database...")
    start()


# Export functions for use by other scripts
{%- if cookiecutter.database_backend == 'mongodb' %}
is_database_ready = is_mongodb_ready
wait_for_database = wait_for_mongodb
{%- elif cookiecutter.database_backend == 'postgresql' %}
is_database_ready = is_postgres_ready  
wait_for_database = wait_for_postgres
{%- endif %}


if __name__ == "__main__":
    app()
{%- endif -%}